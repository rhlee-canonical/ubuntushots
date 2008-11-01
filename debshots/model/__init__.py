# -*- coding: utf-8 -*-

import sqlalchemy as sql
import sqlalchemy.orm as orm
import pylons
import os
from debshots.lib import constants

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
    def large_screenshots(self):
        """Return only the full-sized (up to 800x600) screenshots"""
        return self.screenshots.filter_by(large=True)

    @property
    def small_screenshots(self):
        """Return only the thumbnails (up to 160x120) of the screenshots"""
        return self.screenshots.filter_by(large=False)

#----------

screenshots_table = sql.Table(
    'screenshots', metadata,
    sql.Column('id', sql.Integer, primary_key=True),
    sql.Column('package_id', sql.Integer, sql.ForeignKey('packages.id')),
    sql.Column('uploaddatetime', sql.DateTime(), default=sql.func.now()),
    sql.Column('uploaderhash', sql.Unicode(72)),
    sql.Column('uploaderip', sql.Unicode(15)),
    sql.Column('large', sql.Boolean()), # whether a picture is large or a thumbnail
    sql.Column('status', sql.Integer(), default=constants.SCREENSHOT_STATUS['uploaded']),
        # constant as defined in lib/constants.py
    sql.Column('xsize', sql.Integer()),
    sql.Column('ysize', sql.Integer()),
)

class Screenshot(MyOrm):
    @property
    def directory(self):
        """Return the directory in the filesystem where the screenshot image is saved"""
        return os.path.join(
            pylons.config['debshots.images_directory'],
            self.package.name[0],
            self.package.name
            )

    @property
    def path(self):
        """Return the path in the filesystem to the image file"""
        return os.path.join(
            self.directory,
            str(self.id)
            )

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

orm.mapper(Screenshot, screenshots_table)

orm.mapper(CacheBinaryPackage, cache_binary_packages_table)
