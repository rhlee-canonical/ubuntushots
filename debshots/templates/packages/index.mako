# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-index-header.mako"/>
<%include file="/packages/include-js-lightbox.mako"/>

% if c.packages:
<p>${ c.packages.pager('Page: $link_first $link_previous ~10~ $link_next $link_last') }</p>
<table>
    <tr>
        <th>Package</th>
        <th>Description</th>
        <th>Section</th>
        ##<th>Screenshots</th>
        <th>Homepage</th>
    </tr>
% for package in c.packages:
    <tr>
        <td>
            ${ h.tags.link_to(package.name, h.url_for('package', package=package.name)) }
        </td>
        <td>
            ${ package.description }
        </td>
        <td>
            ${ package.section }
        </td>
        ##<td>
        ##    ${ package.approved_screenshots.count() }
        ##    % if package.unapproved_screenshots.count()>0:
        ##        (${ package.unapproved_screenshots.count() } waiting for approval)
        ##    % endif
        ##</td>
        <td>
            ${ h.tags.link_to(
                package.homepage,
                package.homepage,
                target='_blank') }
        </td>
    </tr>
    ## Second line shows screenshots
    % if package.approved_screenshots.count():
    <tr>
        <td></td>
        <td colspan="3">
            <div class="screenshots">
            % for screenshot in package.approved_screenshots:
            <a class="image" href="${h.url_for('image', id=screenshot.large_image.id)}"
                title="Screenshot of package '${screenshot.package.name}'">
                <img src="${h.url_for('image', id=screenshot.small_image.id)}" alt="Screenshot" />
            </a>
            % endfor
        </td>
    </tr>
    % endif
% endfor
</table>
% else:
<p>No screenshots found.</p>
% endif
