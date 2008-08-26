import logging

from debshots.lib.base import *

log = logging.getLogger(__name__)

class MyController(BaseController):

    def index(self):
        """Show uploaded screenshots for the maintainer that is logged in"""
        return render('/my/index.mako')
