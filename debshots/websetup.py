"""Setup the debshots application"""
import logging
import os
from pylons import config

from debshots.config.environment import load_environment
from debshots.model import meta

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup debshots here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)

    if not os.path.isdir(config['debshots.screenshots_directory']):
        print "Creating screenshots directory"
        os.makedirs(config['debshots.screenshots_directory'])
    else:
        print "Image directory already exists"
