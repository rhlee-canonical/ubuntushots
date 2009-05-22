# -*- coding: utf-8 -*-
## Details and screenshots of a package

<%inherit file="/base.mako"/>

<%include file="/packages/include-js-lightbox.mako"/>

<div class="graybox">
<h1>Package <em>'${ c.package.name }'</em></h1>
<table><tr><td class="noborder">
<h2>Details</h2>
<ul>
    <li><b>Description</b>: ${ c.package.description }</li>
    <li><b>Section</b>: ${ c.package.section }</li>
    % if c.package.homepage:
        <li><b>Homepage</b>:
            ${ h.tags.link_to(
                c.package.homepage,
                c.package.homepage
                ) }
        </li>
    % endif
    <li><b>Package maintainer</b>: ${ c.package.maintainer }</li>
    % if c.package.unapproved_screenshots:
        <li>
            <em>
            ${ len(c.package.unapproved_screenshots) } new screenshot(s) are
            waiting for approval by the admin team.
            </em>
        </li>
    % endif
    <li><a href="http://packages.debian.org/${ c.package.name }">Package
        page on packages.debian.org</a></li>
    <li><a href="http://bugs.debian.org/${ c.package.name }">Bug reports for this package</a>
        </li>
    ## Upload link:
    <li>${ h.tags.link_to('Upload a new screenshot',
            h.url_for('upload', package=c.package.name)) }</li>
</ul>

</td><td class="noborder">

## Debtags
% if c.package.debtags:
    <h2>Tags</h2>
    <ul>
    % for tag in c.package.debtags:
        <li>
            ${ tag.facet_description }: ${ tag.description }
            [<a href="${ h.url_for('packages', debtag=tag.tag) }">Similar packages</a>]
        </li>
    % endfor
    </ul>
% endif
</td></tr></table>
</div>

## Show approved screenshots
<div class="screenshots">
<h1>Available screenshots</h1>
<p><i>
    (These screenshots are licensed under the same terms as
    '${ c.package.name }' itself.)
</i></p>
% if c.package.approved_screenshots:
% for screenshot in c.package.approved_screenshots:
    <div class="screenshot">
    <a class="image" href="${screenshot.large_image_url}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${screenshot.small_image_url}" alt="Screenshot" />
        % if screenshot.version:
        <br />
        Version: ${ screenshot.version }
        % endif
    </a>
    <br />
    ## TODO: Fancy icons :)
    ## Display a message if the screenshot is markedfordelete
    % if screenshot.markedfordelete:
        (Removal was requested.)
    % else:
        ## Admins can remove the screenshots directly:
        % if 'username' in session:
            ${ h.tags.link_to(
                'Remove this screenshot',
                h.url_for('delete_screenshot', screenshot=screenshot.id),
                onclick=h.tags.literal('return confirm(\'Really delete this screenshot?\')')) }
        ## Visitors can mark this package for deletion:
        % else:
            ${ h.tags.link_to(
                'Request removal',
                '#',
                id='markfordelete%s' % screenshot.id,
                onclick="$('#markfordelete-form-%s').show('slow')" % screenshot.id,
                ) }
            ## Hidden field to enter the reason for markedfordelete
            <div id="markfordelete-form-${screenshot.id}" style="display: none">
                ${ h.tags.form(h.url_for('delete_screenshot', screenshot=screenshot.id))}
                Why should it get removed?
                <br />
                ${ h.tags.text('reason', size=20, maxlength=100) }
                <br />
                ${ h.tags.submit('submit', 'Okay') }
                </form>
            </div>
        % endif
    % endif
    </div>
% endfor
% else:
<p>There are no (approved) screenshots for this package yet.</p>
% endif
</div>

## Show screenshots that are not yet approved but uploaded by the
## current visitor (identified by their client cookie hash value).
## This view is not shown if the user is an administrator or otherwise
## the screenshots would also show up in the "not yet approved screenshots"
## section below.
% if ('username' not in session) and (c.package.my_unapproved_screenshots):
<div class="screenshots">
<h1>Your uploaded (not yet approved) screenshots</h1>
% for screenshot in c.package.my_unapproved_screenshots:
    <div class="screenshot">
    <a class="image" href="${screenshot.large_image_url}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${screenshot.small_image_url}" alt="Screenshot" />
    </a>
    % if screenshot.version:
    <br />
    Version: ${ screenshot.version }
    % endif
    ## Allow the visitor to delete their own screenshots
    <br />
    ## TODO: Fancy icons :)
    ${ h.tags.link_to(
        'Delete your screenshot',
        h.url_for('delete_screenshot', screenshot=screenshot.id),
        onclick=h.tags.literal('return confirm(\'Really delete this screenshot?\')')) }
    </div>
% endfor
</div>
% endif

## Show screenshots that are not yet approved (for admins only)
% if 'username' in session and c.package.unapproved_screenshots:
<div class="screenshots">
<h1>Not yet approved screenshots</h1>
% for screenshot in c.package.unapproved_screenshots:
    <div class="screenshot">
    <a class="image" href="${screenshot.large_image_url}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${screenshot.small_image_url}" alt="Screenshot" />
    </a>
    % if screenshot.version:
    <br />
    Version: ${ screenshot.version }
    % endif
    ## Allow the visitor to delete their own screenshots
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
% endif
