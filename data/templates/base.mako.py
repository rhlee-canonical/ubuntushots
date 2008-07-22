from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 3
_modified_time = 1216760604.226119
_template_filename='/home/chaas/projekte/debshots/debshots/templates/base.mako'
_template_uri='/base.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(u'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">\n    <head>\n        <title>screenshots.debian.net</title>\n')
        # SOURCE LINE 9
        __M_writer(u'    </head>\n    <body>\n\n        ')
        # SOURCE LINE 12
        __M_writer(unicode( next.body() ))
        __M_writer(u'\n\n    </body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


