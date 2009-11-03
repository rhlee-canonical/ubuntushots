# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-index-header.mako"/>
<%include file="/packages/include-js-lightbox.mako"/>

% if c.packages:
${ c.packages.pager('Package $page of $page_count - $link_previous ~3~ $link_next') }

% for package in c.packages:
    <h1>Package: ${ package.name }</h1>
    <p>${ package.description }</p>

    <div class="screenshots">
    % for screenshot in package.moderated_screenshots:
    <div class="screenshot">
    <a class="image" href="${screenshot.large_image_url}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${screenshot.small_image_url}" alt="Screenshot" />
    </a>
    <br />
    ## Unapproved screenshot? (approve or delete)
    % if not screenshot.approved:
        ## TODO: Fancy icons :)
        ${ h.tags.link_to(
            'Approve screenshot',
            h.url_for('approve_screenshot', screenshot=screenshot.id, goto=h.url_for())) }
        <br />
        ${ h.tags.link_to(
            'Delete screenshot',
            h.url_for('delete_screenshot', screenshot=screenshot.id, goto=h.url_for()),
            onclick="return confirm('Really delete the screenshot?');") }
    ## Marked for delete? (keep or delete)
    % elif screenshot.markedfordelete:
        Removal requested (<em>${screenshot.delete_reason}</em>)
        <br />
        ${ h.tags.link_to(
            'Keep the screenshot',
            h.url_for('keep_screenshot', screenshot=screenshot.id, goto=h.url_for())) }
        <br />
        ${ h.tags.link_to(
            'Delete screenshot',
            h.url_for('delete_screenshot', screenshot=screenshot.id, goto=h.url_for()),
            onclick="return confirm('Really delete the screenshot?');") }
    % endif
    </div>
    % endfor
    </div>
% endfor
</table>
% else:
<p>There are no screenshots awaiting moderation.</p>
% endif
