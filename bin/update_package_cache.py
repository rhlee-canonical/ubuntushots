#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extract the maintainers' email addresses and package names from Sources.gz"""
# Mimics: zcat Sources.gz | grep-dctrl -FMaintainer,Uploaders foo@bar -ns package
import logging
import os
import urllib
import sys
import re
from paste.deploy import appconfig
from pylons import config
from debian_bundle import debian_support, deb822
import subprocess
from debshots.config.environment import load_environment

tempfile = '/tmp/sources'
log = logging.getLogger(__name__)

def main():
    log.info("Initalising Pylons environment...")

    conf = appconfig('config:' + sys.argv[1])
    load_environment(conf.global_conf, conf.local_conf)

    # Initialize database
    from debshots import model

    # ... empty database (we are in a transaction - no harm done)

    # Remove old tempfile
    if os.path.isfile(tempfile):
        os.unlink(tempfile)

    # Get Sources.gz
    #for component in ('main', 'non-free', 'contrib'):
    for component in ('contrib','non-free'): # TODO: only testing
        url = "%s/dists/unstable/%s/source/Sources" % \
            (config['debshots.debian_mirror'], component)
        log.info("Fetching URL: %s" % url)
        debian_support.downloadFile(url, tempfile)

        log.info("Purging package cache database")
        delete = model.cache_maintainers_table.delete()
        model.Session.execute(delete)
        model.Session.commit()

        log.info("Parsing Sources file into database cache")
        for pkg in deb822.Dsc.iter_paragraphs(file(tempfile)):
            if 'Maintainer' in pkg:
                log.debug("---------")
                log.debug("Source package:", pkg['package'])
                match = re.match(r'(.+?)\<(.+?)\>', pkg['maintainer'])
                assert match, "Couldn't parse email address from maintainer entry (%s)" % pkg['maintainer']
                maint_name, maint_email = match.groups()
                log.debug("Maintainer:    %s" % maint_name)
                log.debug("Email:         %s" % maint_email)
                log.debug("Binary packages:")
                for binpkg in pkg['binary'].split(', '):
                    log.debug("- %s" % binpkg)

                # Is there a database entry for this maintainer already?
                db_maintainer = model.CacheMaintainer.q().filter_by(email=maint_email.decode('utf8')).first()
                if not db_maintainer:
                    # new maintainer - create the database entry
                    db_maintainer = model.CacheMaintainer(
                        name = maint_name.decode('utf8'),
                        email = maint_email.decode('utf8'),
                    )
                    model.Session.save(db_maintainer)

                # Create source package
                db_srcpkg = model.CacheSourcePackage(
                    name = pkg['package'].decode('utf8'))
                model.Session.save(db_srcpkg)
                db_maintainer.source_packages.append(db_srcpkg)

                # Create binary packages
                for binpkg in pkg['binary'].split(', '):
                    db_binpkg = model.CacheBinaryPackage(
                        name = binpkg.decode('utf8'))
                    model.Session.save(db_binpkg)
                    db_srcpkg.binary_packages.append(db_binpkg)

        model.Session.commit()

if __name__ == '__main__':
    main()
