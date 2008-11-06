# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-index-header.mako"/>
<%include file="/packages/include-js-lightbox.mako"/>

% if c.packages:
${ c.packages.pager('Package $page of $page_count - $link_previous ~3~ $link_next') }
% for package in c.packages:
    <h1>${ package.name }</h1>

    <div class="screenshots">
    % for screenshot in package.uploaded_screenshots:
    <div class="screenshot">
    <a class="image" href="${h.url_for('image', id=screenshot.large_image.id)}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${h.url_for('image', id=screenshot.small_image.id)}" alt="Screenshot" />
    </a>
    </div>
    % endfor
    </div>
% endfor
</table>
% else:
<p>There are no screenshots awaiting moderation.</p>
% endif
