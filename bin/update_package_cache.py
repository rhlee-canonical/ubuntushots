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

logging.basicConfig(
    #level=logging.DEBUG,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
    )

def main():
    logging.info("Initalising Pylons environment...")

    conf = appconfig('config:' + sys.argv[1])
    load_environment(conf.global_conf, conf.local_conf)

    # Initialize database
    from debshots import model

    # ... empty database (we are in a transaction - no harm done)
    logging.info("Purging package cache database")
    delete = model.cache_binary_packages_table.delete()
    model.Session.execute(delete)
    logging.info("Purging done")

    # Remove old tempfile
    if os.path.isfile(tempfile):
        os.unlink(tempfile)

    # Get Packages.gz (lists of binary packages)
    #for arch in ('alpha', 'amd64', 'arm', 'armel', 'hppa', 'hurd-i386', 'i386',
        #'ia64', 'm68k', 'mips', 'mipsel', 'powerpc', 's390', 'sparc'): # TODO: only testing
    for arch in ('i386',): # TODO: only testing
        for component in ('main', 'non-free', 'contrib'):
        #for component in ('contrib',): # TODO: only testing
            url = "%s/dists/unstable/%s/binary-%s/Packages" % \
                (config['debshots.debian_mirror'], component, arch)
            logging.info("Fetching URL: %s" % url)
            debian_support.downloadFile(url, tempfile)

            logging.info("Parsing Packages.gz file into database cache")
            for pkg in deb822.Dsc.iter_paragraphs(file(tempfile)):
                logging.debug("---------")
                logging.info("Package:       %s " % pkg['package'])

                match = re.match(r'(.+?) *\<(.+?)\>', pkg['maintainer'])
                assert match, "Couldn't parse email address from maintainer entry (%s)" % pkg['maintainer']
                maint_name, maint_email = match.groups()

                logging.debug("Maintainer:    %s" % maint_name)
                logging.debug("Email:         %s" % maint_email)

                # Get first line of the description
                description = pkg['description'].split('\n')[0]
                logging.debug("Description:   %s" % description)

                # Skip adding it to the database if it's already recorded
                if model.CacheBinaryPackage.q().filter_by(name=pkg['package'].decode('utf8')).first():
                    logging.debug('(exists in the database already - skipping)')
                    continue

                db_binpkg = model.CacheBinaryPackage(
                    name = pkg['Package'][:100].decode('utf8'),
                    description = description[:80].decode('utf8'),
                    section = pkg['Section'].decode('utf8'),
                    maintainer = maint_name[:100].decode('utf8'),
                    homepage = pkg.get('Homepage', '')[:200].decode('utf8'),
                    )
                model.Session.save(db_binpkg)

    logging.info("Committing to database")
    model.Session.commit()

if __name__ == '__main__':
    main()
