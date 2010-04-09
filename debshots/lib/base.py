"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import validate, jsonify
from pylons import request, response, session, tmpl_context as c, config
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

import debshots.lib.helpers as h
from debshots.model import meta
from debshots.lib import my
from debshots import model
import logging
log = logging.getLogger(__name__)

db = model.meta.Session

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # Make sure that there is 'messages' entry in the cookie session
        if 'messages' not in session: session['messages']=[]

        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
