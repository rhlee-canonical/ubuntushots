# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-index-header.mako"/>

% if c.packages:
<p>${ c.packages.pager('Page: $link_first $link_previous ~2~ $link_next $link_last') }</p>
<table>
    <tr>
        <th>Package</th>
        <th>Description</th>
        <th>Section</th>
        <th>Screenshots</th>
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
            ${ package.approved_screenshots.count() }
            % if package.unapproved_screenshots.count()>0:
                (${ package.unapproved_screenshots.count() } waiting for approval)
            % endif
        </td>
        <td>
            ${ h.tags.link_to(
                package.cachebinarypackage.homepage,
                package.cachebinarypackage.homepage,
                target='_blank') }
        </td>

    </tr>
% endfor
</table>
% else:
<p>No screenshots found.</p>
% endif
