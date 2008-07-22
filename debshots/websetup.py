"""Setup the debshots application"""
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
    print "Create database tables"
    model.metadata.create_all(bind=config['pylons.g'].sa_engine)

    if not os.path.isdir(config['debshots.images_directory']):
        print "Creating image directory"
        os.makedirs(config['debshots.images_directory'])
    else:
        print "Image directory already exists"
