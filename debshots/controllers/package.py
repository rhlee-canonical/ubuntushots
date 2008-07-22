# -*- coding: utf-8 -*-
import logging

from debshots.lib.base import *

log = logging.getLogger(__name__)

class PackageController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
        return 'Hello World'
