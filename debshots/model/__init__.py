# -*- coding: utf-8 -*-

import sqlalchemy as sql
import sqlalchemy.orm as orm
import pylons

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

class Package(MyOrm): pass

#----------

screenshots_table = sql.Table(
    'screenshots', metadata,
    sql.Column('id', sql.Integer, primary_key=True),
    sql.Column('package_id', sql.Integer, sql.ForeignKey('packages.id')),
    sql.Column('uploaddatetime', sql.DateTime(), default=sql.func.now()),
    sql.Column('uploaderhash', sql.Unicode(50)),
    sql.Column('uploaderip', sql.Unicode(15)),
    sql.Column('large', sql.Boolean()), # whether a picture is large or a thumbnail
    sql.Column('approved', sql.Boolean(), default=False), # whether a picture has been approved by an admin
    sql.Column('xsize', sql.Integer()),
    sql.Column('ysize', sql.Integer()),
)

class Screenshot(MyOrm): pass

#----------

orm.mapper(Package, packages_table, order_by=packages_table.c.name,
    properties={
        'screenshots':orm.relation(
            Screenshot,
            backref=orm.backref('package', uselist=False),
            cascade='all, delete-orphan')
        })

orm.mapper(Screenshot, screenshots_table)

orm.mapper(CacheBinaryPackage, cache_binary_packages_table)
