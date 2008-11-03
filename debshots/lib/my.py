# -*- coding: utf-8 -*-

import pylons
import logging
import formencode

log = logging.getLogger(__name__)

def validate(schema, **state_kwargs):
    """Validate a formencode schema. Similar to @validate.

    On success return a dictionary of values from request.params.
    On failure returns a formencode.Invalid exception."""
    # State-Objekt anlegen
    if state_kwargs:
        state = State(**state_kwargs)
    else:
        state = None

    return schema.to_python(pylons.request.params, state)

def htmlfill(html, exception_error=None):
    """Fills an HTML string with error messages from the last formencode validation.

    'html' contains the HTML page with the form (e.g. from render()).
    'exception_error' contains the formencode.Invalid exception."""
    if exception_error:
        log.debug('my.htmlfill formencode exception: %s' % (exception_error,))
    return formencode.htmlfill.render(
        form=html,
        defaults=pylons.request.params,
        errors=(exception_error and exception_error.unpack_errors()),
        encoding=pylons.response.determine_charset()
    )

def client_ip():
    """Return the IP address of the client."""
    return unicode(pylons.request.environ['REMOTE_ADDR'])

def client_cookie_hash():
    """Return the cookie hash used for the cookie-based session"""
    cookie_hash = unicode(pylons.request.cookies[pylons.config['beaker.session.key']])
    log.debug("Client cookie hash is: %s" % cookie_hash)
    return cookie_hash

def authorized_for_screenshot(screenshot):
    """Check if a user is authorized to view a certain screenshot

    Either the screenshot was uploaded by the same client (checks cookie hash)
    or the user is an admin."""
    if client_cookie_hash() == screenshot.uploaderhash:
        log.debug("User is authorized to view screenshot '%s' (same cookie)" % screenshot)
        return True

    if 'username' in pylons.session:
        log.debug("User is authorized to view screenshot '%s' (admin logged in)" % screenshot)
        return True

    return False
