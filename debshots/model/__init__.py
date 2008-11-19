# -*- coding: utf-8 -*-

import sqlalchemy as sql
import sqlalchemy.orm as orm
import pylons
import os
import md5
from debshots.lib import my
from routes import url_for

import logging
log = logging.getLogger(__name__)

# Global session manager.  Session() returns the session object
# appropriate for the current web request.
Session = orm.scoped_session(orm.sessionmaker(
    autoflush=True,
    transactional=True,
    bind=pylons.config['pylons.g'].sa_engine))

# Global metadata
metadata = sql.MetaData()

# Base class for object-relational mappers
class MyOrm(object):
    @classmethod
    def q(self):
        """Create Query object of an ORM class"""
        return Session.query(self)

    # from http://www.sqlalchemy.org/trac/wiki/UsageRecipes/GenericOrmBaseClass
    def __init__(self, **kw):
        for key in kw:
            if key in self.c:
                setattr(self, key, kw[key])
            else:
                raise AttributeError('Cannot set attribute which is not column in mapped table: %s' % (key,))

    def update(self, update_dict, ignore_missing_columns=True):
        """Update ORM object attributes"""
        for key in update_dict:
            if key in self.c:
                setattr(self, key, update_dict[key])
            elif not ignore_missing_columns:
                raise AttributeError('Cannot set attribute which is not column in mapped table: %s' % (key,))

    def __repr__(self):
        atts = []
        for key in self.c.keys():
            if key in self.__dict__:
                if not (hasattr(self.c.get(key).default, 'arg') and
                        getattr(self.c.get(key).default, 'arg') == getattr(self, key)):
                    atts.append( (key, getattr(self, key)) )

        return self.__class__.__name__ + '(' + ', '.join(x[0] + '=' + repr(x[1]) for x in atts) + ')'

# Table containing Debian packages
#
# This table gets updated by the debshots-update-packages script
packages_table = sql.Table(
    'packages', metadata,
    sql.Column('id', sql.Integer, primary_key=True),
    sql.Column('name', sql.Unicode(100), unique=True),
    sql.Column('description', sql.Unicode(80)),
    sql.Column('section', sql.Unicode(50)),
    sql.Column('maintainer', sql.Unicode(100)),
    sql.Column('maintainer_email', sql.Unicode(100)),
    sql.Column('homepage', sql.Unicode(200)),
    sql.Column('version', sql.Unicode(50)),
)

class Package(MyOrm):
    @property
    def unapproved_screenshots(self):
        """Return a list of freshly uploaded (not yet approved) screenshots for this package"""
        return [ss for ss in self.screenshots if not ss.approved]

    @property
    def approved_screenshots(self):
        """Return a list of approved (by a moderator) screenshots for this package"""
        return [ss for ss in self.screenshots if ss.approved]

    @property
    def markedfordelete_screenshots(self):
        """Return a list of markedfordelete (not yet approved for deletion) screenshots for this package"""
        return [ss for ss in self.screenshots if ss.markedfordelete]

    @property
    def my_screenshots(self):
        """Return a list of screenshots uploaded by the current user.

        As users do not need to login before they can upload screenshots
        they are only identified by their client cookie. So this method
        returns all screenshots that have the same cookie hash value
        stored as the current cookie sent by the browser."""
        return [ss for ss in self.screenshots if ss.uploaderhash==my.client_cookie_hash()]

    @property
    def my_or_approved_screenshots(self):
        """Return a list of the user's own or any approved screenshots"""
        return [ss for ss in self.screenshots if (ss.approved or ss.uploaderhash==my.client_cookie_hash())]

    @property
    def moderated_screenshots(self):
        """Return a list of freshly uploaded or marked for delete screenshots of this package"""
        return [ss for ss in self.screenshots if (not ss.approved or ss.markedfordelete)]

def packages_with_moderated_screenshots():
    """Return a list of packages with screenshots that need moderation"""
    return Package.q().join('screenshots').filter(
        (Screenshot.c.approved==False)
        |
        (Screenshot.c.markedfordelete==True)
    )

def packages_without_screenshots():
    """Return packages that do not have screenshots yet"""
    packages = Package.q()
    packages = packages.filter(~Package.id.in_(
        sql.select([Screenshot.package_id])
        ))
    return packages

#----------

image_types = [
    {'size': (160,120), 'extension': 'small'},
    {'size': (800,600), 'extension': 'large'}
]

# A screenshot here is an entry for each uploaded screenshot.
screenshots_table = sql.Table(
    'screenshots', metadata,
    sql.Column('id', sql.Integer, primary_key=True),
    sql.Column('package_id', sql.Integer, sql.ForeignKey('packages.id')),
    sql.Column('version', sql.Unicode(50)),
    sql.Column('uploaddatetime', sql.DateTime(), default=sql.func.now()),
    sql.Column('uploaderhash', sql.Unicode(72)),
    sql.Column('uploaderip', sql.Unicode(15)),
    sql.Column('approved', sql.Boolean(), default=False),
    sql.Column('markedfordelete', sql.Boolean(), default=False),
    sql.Column('delete_reason', sql.Unicode(100)),
)


class Screenshot(MyOrm):
    @property
    def large_image_url(self):
        if self.approved:
            package_name = self.package.name
            return url_for('image', package_inital=package_name[0], package=package_name, id=self.id, size='large')
        return url_for('unapproved_image', id=self.id, size='large')

    @property
    def small_image_url(self):
        if self.approved:
            package_name = self.package.name
            return url_for('image', package_inital=package_name[0], package=package_name, id=self.id, size='small')
        return url_for('unapproved_image', id=self.id, size='small')

    @property
    def directory(self):
        """Return the directory in the filesystem where the screenshot is saved"""
        if self.approved:
            directory = 'approved'
        else:
            directory = 'unapproved'
        return os.path.join(
            pylons.config['debshots.screenshots_directory'],
            directory,
            self.package.name[0],
            self.package.name
            )

    def image_path(self, size):
        """Return the path to a certain image file on disk.

        'size' can be 'large' or 'small'."""
        assert size in ('small', 'large')
        return os.path.join(self.directory, '%s_%s.png' % (self.id, size))

    @property
    def image_paths(self):
        """Returns a list of paths to the images of all (both) sizes"""
        result = []
        for image_type in image_types:
            result.append(os.path.join(
                self.directory,
                '%s_%s.png' % (self.id, image_type['extension'])
                ))
        return result

def moderated_screenshots():
    """Return a list of freshly uploaded or marked for delete screenshots"""
    return Screenshot.q().filter(
        (Screenshot.approved==False)
        |
        (Screenshot.markedfordelete==True)
    )

def newest_screenshots():
    """Return a query of all approved screenshots ordered by upload date"""
    screenshots = Screenshot.q().filter_by(approved=True)
    newest_screenshots = screenshots.order_by(Screenshot.uploaddatetime.desc())
    newest_screenshots = newest_screenshots.options(orm.eagerload('package'))
    return newest_screenshots

#----------

# Table of admin users
# (screenshots can be uploaded by anyone - but they have to be approved by an admin)
admins_table = sql.Table(
    'admins', metadata,
    sql.Column('id', sql.Integer, primary_key=True),
    sql.Column('username', sql.Unicode(20), unique=True),
    sql.Column('passwordhash', sql.Unicode(32)), # MD5 hash of the admin's password
)

class Admin(MyOrm):
    def setpassword(self, newpassword):
        """Set an admin's password to a new value"""
        self.passwordhash = md5.md5(newpassword+pylons.config['debshots.md5salt']).hexdigest()

#----------

orm.mapper(Package, packages_table, order_by=packages_table.c.name,
    properties={
        'screenshots':orm.relation(
            Screenshot,
            backref=orm.backref('package', uselist=False),
            cascade='all, delete-orphan',
            ),
        })

orm.mapper(Screenshot, screenshots_table)

orm.mapper(Admin, admins_table)
