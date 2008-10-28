# -*- coding: utf-8 -*-
import logging

from debshots.lib.base import *

log = logging.getLogger(__name__)

class PackagesController(BaseController):

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

    def ajax_autocomplete_packages(self):
        """Get a list of packages for the autocompleter"""
        query = request.params.get('q')
        packages = model.CacheBinaryPackage.q().filter(model.CacheBinaryPackage.name.startswith(query))[:30]
        return '\n'.join(["%s|%s" % (package.name, package.description) for package in packages])
