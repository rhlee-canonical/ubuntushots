"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
from pylons import c, cache, config, g, request, response, session
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons.templating import render

import debshots.lib.helpers as h
import debshots.model as model
from debshots.lib import my, constants

import logging
log = logging.getLogger(__name__)

db = model.Session

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # Create a dummy session so we have hash to identify the client
        #log.debug("Session: %r" % session)
        session.save()
        #log.debug("Cookies: %r" % request.cookies)

        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            #c.controller = request.environ['pylons.routes_dict']['controller']
            #c.maintainer_id = session.get('maintainer')
            #c.maintainer = model.Session.query(model.Maintainer).filter_by(id=c.maintainer_id).first()
            return WSGIController.__call__(self, environ, start_response)
        finally:
            model.Session.remove()

# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']
