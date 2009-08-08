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
from routes.util import url_for
from debshots.lib import my
