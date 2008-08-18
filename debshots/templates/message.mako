# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<div class="textbox">
    % if c.title:
    <h1>${c.title}</h1>
    % endif
    % if c.message:
    <p>
        ${c.message}
    </p>
    % endif
