# -*- coding: utf-8 -*-

import sqlalchemy as sql
import sqlalchemy.orm as orm
import pylons
import os
import md5
from debshots.lib import constants, my

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

#----------
# Cache created from Sources.gz files to get quick access to available binary packages
cache_binary_packages_table = sql.Table(
    'cache_binary_packages', metadata,
    sql.Column('id', sql.Integer, primary_key=True),
    sql.Column('name', sql.Unicode(100), index=True, unique=True),
    sql.Column('description', sql.Unicode(80)),
    sql.Column('section', sql.Unicode(50)),
    sql.Column('maintainer', sql.Unicode(100)),
    sql.Column('homepage', sql.Unicode(200)),
)

class CacheBinaryPackage(MyOrm): pass

#----------

packages_table = sql.Table(
    'packages', metadata,
    sql.Column('id', sql.Integer, primary_key=True),
    sql.Column('name', sql.Unicode(100), unique=True),
)

class Package(MyOrm):
    @property
    def uploaded_screenshots(self):
        """Return a list of freshly uploade (not yet approved) screenshots"""
        return self.screenshots.filter_by(status=constants.SCREENSHOT_STATUS['uploaded'])

    @property
    def approved_screenshots(self):
        """Return a list of approved (by a moderator) screenshots"""
        return self.screenshots.filter_by(status=constants.SCREENSHOT_STATUS['approved'])

    @property
    def markedfordelete_screenshots(self):
        """Return a list of markedfordelete (not yet approved for deletion) screenshots"""
        return self.screenshots.filter_by(status=constants.SCREENSHOT_STATUS['markedfordelete'])

    @property
    def my_screenshots(self):
        """Return a list of screenshots uploaded by the current user.

        As users do not need to login before they can upload screenshots
        they are only identified by their client cookie. So this method
        returns all screenshots that have the same cookie hash value
        stored as the current cookie sent by the browser."""
        return self.screenshots.filter_by(uploaderhash=my.client_cookie_hash())

#----------

# A screenshot here is an entry for each uploaded image. It does not contain the
# image itself. Rather it has a dependent images_table that stores this screenshot
# in different sizes (thumbnail and full-sized).
screenshots_table = sql.Table(
    'screenshots', metadata,
    sql.Column('id', sql.Integer, primary_key=True),
    sql.Column('package_id', sql.Integer, sql.ForeignKey('packages.id')),
    sql.Column('uploaddatetime', sql.DateTime(), default=sql.func.now()),
    sql.Column('uploaderhash', sql.Unicode(72)),
    sql.Column('uploaderip', sql.Unicode(15)),
    # constant as defined in lib/constants.py:
    sql.Column('status', sql.Integer(), default=constants.SCREENSHOT_STATUS['uploaded']),
)

class Screenshot(MyOrm):
    @property
    def directory(self):
        """Return the directory in the filesystem where the screenshot images are saved"""
        return os.path.join(
            pylons.config['debshots.images_directory'],
            self.package.name[0],
            self.package.name
            )

    @property
    def small_image(self):
        """Return the image object for the thumbnail"""
        return Image.q().filter_by(screenshot=self).filter_by(large=False).first()

    @property
    def large_image(self):
        """Return the image object for the full-sized image"""
        return Image.q().filter_by(screenshot=self).filter_by(large=True).first()

#----------

# Each screenshot points to two 'images'. There is a small and a large image entry.
# The actual PNG files are stored on disk.
images_table = sql.Table(
    'images', metadata,
    sql.Column('id', sql.Integer, primary_key=True),
    sql.Column('screenshot_id', sql.Integer, sql.ForeignKey('screenshots.id')),
    sql.Column('large', sql.Boolean()), # whether a picture is full-sized (True) or a thumbnail (False)
    sql.Column('xsize', sql.Integer()), # width of the image
    sql.Column('ysize', sql.Integer()), # height of the image
)

class Image(MyOrm):
    @property
    def path(self):
        """Return the path in the filesystem to the image file"""
        return os.path.join(
            self.screenshot.directory,
            str(self.id)
            )

#----------

# Table of admin users
# (images can be uploaded by anyone - but they have to be approved by an admin)
users_table = sql.Table(
    'users', metadata,
    sql.Column('id', sql.Integer, primary_key=True),
    sql.Column('username', sql.Unicode(20), unique=True),
    sql.Column('passwordhash', sql.Unicode(32)), # MD5 hash of the user's password
)

class User(MyOrm):
    def setpassword(self, newpassword):
        """Set a user's password to a new value"""
        self.passwordhash = md5.md5(newpassword).hexdigest()

#----------

orm.mapper(Package, packages_table, order_by=packages_table.c.name,
    properties={
        'screenshots':orm.relation(
            Screenshot,
            backref=orm.backref('package', uselist=False),
            cascade='all, delete-orphan',
            lazy='dynamic'
            ),
        # Create a reference to the package cache by looking for package of the same name
        'cachebinarypackage':orm.relation(
            CacheBinaryPackage,
            primaryjoin=(packages_table.c.name==cache_binary_packages_table.c.name),
            foreign_keys=[cache_binary_packages_table.c.name],
            uselist=False
            ),
        })

orm.mapper(Image, images_table)

orm.mapper(Screenshot, screenshots_table,
    properties={
        'images':orm.relation(
            Image,
            backref=orm.backref('screenshot', uselist=False),
            cascade='all, delete-orphan',
            #lazy='dynamic'
        )
    })

orm.mapper(CacheBinaryPackage, cache_binary_packages_table)

orm.mapper(User, users_table)
