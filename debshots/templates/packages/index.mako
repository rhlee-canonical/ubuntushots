# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-index-header.mako"/>
<%include file="/packages/include-js-lightbox.mako"/>

% if not c.packages:
<p>No screenshots found.</p>
<% return %>
% endif

<p>${ c.packages.pager('Page: $link_first $link_previous ~10~ $link_next $link_last') }</p>
<table>
    <tr>
        <th>Package</th>
        <th>Description</th>
        <th>Section</th>
        ##<th>Screenshots</th>
        <th>Homepage</th>
        <th>Contribute</th>
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
        ## Show link to upload screenshots
        <td>
            ${ h.tags.link_to('Upload a screenshot', h.url_for('upload', package=package.name)) }
        </td>

    </tr>
    ## Second line shows screenshots
    % if package.my_or_approved_screenshots:
    <tr>
        <td></td>
        <td colspan="4">
            <div class="screenshots">
        % for screenshot in package.my_or_approved_screenshots:
            <a class="image" href="${screenshot.large_image_url}"
                title="Screenshot of package '${screenshot.package.name}'">
                <img src="${screenshot.small_image_url}" alt="Screenshot" />
            </a>
        % endfor
        </td>
    </tr>
    % endif
% endfor
</table>
<p>${ c.packages.pager('Page: $link_first $link_previous ~10~ $link_next $link_last') }</p>
