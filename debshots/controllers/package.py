# -*- coding: utf-8 -*-
import logging

from debshots.lib.base import *

log = logging.getLogger(__name__)

class PackageController(BaseController):

    #def index(self):
    #    """Show a list of packages with screenshots"""
    #    packages = model.Package.q()
    #    c.packages = h.paginate.Page(packages,
    #        page=int(request.params.get('page_nr')))
    #    return render('/packages/index.mako')

    def upload(self):
        """Show package upload dialog"""
        return render('/packages/upload.mako')

    #def uploadfile(self):
        #"""