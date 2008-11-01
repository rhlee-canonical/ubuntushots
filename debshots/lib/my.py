# -*- coding: utf-8 -*-

import pylons
import logging
import formencode
from debshots import model

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
    return unicode(pylons.request.cookies[pylons.config['beaker.session.key']])

# Formencode validators
class ValidatorDebianPackage(formencode.FancyValidator):
    """formencode validator that makes sure a certain Debian package exists (by its name)"""
    messages = {
            'not_exists' : \
                u'There is no Debian package with that name.',
            }

    def _to_python(self, value, state):
        cachepackage = model.CacheBinaryPackage.q().filter_by(name=value).first()
        if not cachepackage:
            raise formencode.Invalid(self.message("not_exists", state), value, state)
        return cachepackage
