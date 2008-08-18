# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<h1>Packages</h1>

% if c.packages:
<ul>
% for package in c.packages:
    <li>
    ${ package.name }
    </li>
% endfor
</ul>
% else:
<p>No packages are in the database yet.</p>
% endif
