# -*- coding: utf-8 -*-

import pylons

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
