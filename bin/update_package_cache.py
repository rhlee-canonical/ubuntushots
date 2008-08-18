"""Extract the maintainers' email addresses and package names from Sources.gz"""
# zcat Sources.gz | grep-dctrl -FMaintainer,Uploaders foo@bar -ns package
import logging
import os

from paste.deploy import appconfig
from pylons import config

from debshots.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup debshots here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)

    # Initialize database
    from debshots import model

    # ... empty database (we are in a transaction - no harm done)

    # Get Sources.gz
    for component in ('main', 'non-free', 'contrib'):
        url = "%s/dists/%s/source/Sources.bz2" % (config['debshots.debian_mirror'], component)
        # ... get url
        # ... grep-dctrl...
        # ... put into database
