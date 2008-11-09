# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-index-header.mako"/>
<%include file="/packages/include-js-lightbox.mako"/>

% if c.packages:
${ c.packages.pager('Package $page of $page_count - $link_previous ~3~ $link_next') }
% for package in c.packages:
    <h1>${ package.name }</h1>

    <div class="screenshots">
    % for screenshot in package.unapproved_screenshots:
    <div class="screenshot">
    <a class="image" href="${h.url_for('image', id=screenshot.large_image.id)}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${h.url_for('image', id=screenshot.small_image.id)}" alt="Screenshot" />
    </a>
    <br />
    ## TODO: Fancy icons :)
    ${ h.tags.link_to(
        'Approve screenshot',
        h.url_for('approve_screenshot', screenshot=screenshot.id, goto=h.url_for())) }
    <br />
    ${ h.tags.link_to(
        'Delete screenshot',
        h.url_for('delete_screenshot', screenshot=screenshot.id, goto=h.url_for()),
        onclick=h.tags.literal('return confirm(\'Really delete this screenshot?\')')) }

    </div>
    % endfor
    </div>
% endfor
</table>
% else:
<p>There are no screenshots awaiting moderation.</p>
% endif
