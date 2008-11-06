# -*- coding: utf-8 -*-
## Details and screenshots of a package
<%inherit file="/base.mako"/>

<%include file="/packages/include-index-header.mako"/>

<div class="graybox">
<h1>Package <em>'${ c.package.name }'</em></h1>
<ul>
    <li><b>Description</b>: ${ c.package.cachebinarypackage.description }</li>
    <li><b>Section</b>: ${ c.package.cachebinarypackage.section }</li>
    % if c.package.cachebinarypackage.homepage:
        <li><b>Homepage</b>: ${ c.package.cachebinarypackage.homepage }</li>
    % endif
    <li><b>Package maintainer</b>: ${ c.package.cachebinarypackage.maintainer }</li>
    % if c.package.uploaded_screenshots.count()>0:
        <li>
            <em>
            ${ c.package.uploaded_screenshots.count() } new screenshots are
            waiting for approval by the admin team.
            </em>
        </li>
    % endif
</ul>
</div>

## Show approved screenshots
<div class="screenshots">
<h1>Screenshots</h1>
% if c.package.approved_screenshots.count():
% for screenshot in c.package.approved_screenshots:
    <div class="screenshot">
    <a class="image" href="${h.url_for('image', id=screenshot.large_image.id)}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${h.url_for('image', id=screenshot.small_image.id)}" alt="Screenshot" />
    </a>
    <br />
    ## TODO: Fancy icons :)
    ${ h.tags.link_to(
        'Have this screenshot removed',
        h.url_for('delete_screenshot', screenshot=screenshot.id),
        onclick=h.tags.literal('return confirm("Really delete this screenshot?")')) }
    </div>
% endfor
% else:
<p>There are no approved screenshots for this package yet.</p>
% endif
</div>

## TODO: Is there a way to clear via CSS?
<br clear="all" />

## Show screenshots that are not yet approved but uploaded by the
## current user (identified by their client cookie hash value)
% if c.package.my_screenshots.count():
<div class="screenshots">
<h1>Your uploaded screenshots</h1>
% for screenshot in c.package.my_screenshots:
    <div class="screenshot">
    <a class="image" href="${h.url_for('image', id=screenshot.large_image.id)}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${h.url_for('image', id=screenshot.small_image.id)}" alt="Screenshot" />
    </a>
    ## Allow the user to delete their own screenshots
    <br />
    ## TODO: Fancy icons :)
    ${ h.tags.link_to(
        'Delete your screenshot',
        h.url_for('delete_screenshot', screenshot=screenshot.id),
        onclick=h.tags.literal('return confirm("Really delete this screenshot?")')) }
    </div>
% endfor
</div>
% endif
