# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<div class="graybox">
<h1>Browsing screenshots</h1>
<p>
    By name
    |
    By category
    |
    Without screenshots
    |
    Moderation queue
</p>
</div>

% if c.packages:
<table>
    <tr>
        <th>Package</th>
        <th>Description</th>
        <th>Section</th>
        <th>Homepage</th>
    </tr>
% for package in c.packages:
    <tr>
        <td>
            ${ h.tags.link_to(package.name, h.url_for('package', package=package.name)) }
        </td>
        <td>
            ${ package.cachebinarypackage.description }
        </td>
        <td>
            ${ package.cachebinarypackage.section }
        </td>
        <td>
            ${ h.tags.link_to(package.cachebinarypackage.homepage, package.cachebinarypackage.homepage) }
        </td>

    </tr>
% endfor
</table>
## TODO: pager
% else:
<p>There are no screenshots yet.</p>
% endif
