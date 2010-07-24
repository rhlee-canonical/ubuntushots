"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from webhelpers import *
from webhelpers.html import tags
from webhelpers import paginate
#from pylons.controllers.util import url_for
from pylons import url
from routes.util import url_for
from debshots.lib import my

def package_page_link(package):
    """Return the URL to the package page depending on the origin.

    For Ubuntu packages it points to packages.ubuntu.com while for all other packages it
    points to packages.debian.org."""
    if package.origin is not None and package.origin.lower()=='ubuntu':
        return tags.link_to("Package page on ubuntu.com", "http://packages.ubuntu.com/%s" % package.name)
    else:
        return tags.link_to("Package page on debian.org", "http://packages.debian.org/%s" % package.name)

def bugs_page_link(package):
    """Return the URL to the bug reports page depending on the origin.

    For Ubuntu packages it points to edge.launchpad.net while for all other packages it
    points to bugs.debian.org."""
    if package.origin is not None and package.origin.lower()=='ubuntu':
        return tags.link_to("Bug reports", "https://launchpad.net/distros/ubuntu/+source/%s/+bugs" % package.name)
    else:
        return tags.link_to("Bug reports", "http://bugs.debian.org/%s" % package.name)
