import logging

from debshots.lib.base import *

log = logging.getLogger(__name__)

class UploadController(BaseController):

    def index(self):
        """Show picture upload form"""
        return render('/upload/form.mako')
