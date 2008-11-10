# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<div class="error-border">
% if c.code == 401:
    <h1>Error 401 - Authentication required</h1>
    <p>
        You need to be logged in to use this function.
    </p>
% elif c.code == 403:
    <h1>Error 403 - Not authorized</h1>
    <p>
        You do not have the permission to use this function.
    </p>
% elif c.code == 404:
    <h1>Error 404 - Page not found</h1>
    <p>
        The page you requested does not exist.
    </p>
% else:
    <h1>Internal error ${ c.code }</h1>
    <p>
        An unexpected error occured in this application.
        The administrator will get a detailed report about the
        error situation. We appreciate if you give us more
        information how this error situation happened.
    </p>
% endif
</div>
