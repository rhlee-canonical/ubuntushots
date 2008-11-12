# -*- coding: utf-8 -*-
## Details and screenshots of a package
<%inherit file="/base.mako"/>

<%include file="/packages/include-js-lightbox.mako"/>

<script type="application/x-javascript">
    $(document).ready(function() {
        $('#markfordelete').click(
            function () {
                $('#markfordelete-form').show('slow');
                $('#markfordelete-reason').focus();
            }
        )
    });
</script>


<div class="graybox">
<h1>Package <em>'${ c.package.name }'</em></h1>
<ul>
    <li><b>Description</b>: ${ c.package.description }</li>
    <li><b>Section</b>: ${ c.package.section }</li>
    % if c.package.homepage:
        <li><b>Homepage</b>:
            ${ h.tags.link_to(
                c.package.homepage,
                c.package.homepage,
                target='_blank') }
        </li>
    % endif
    <li><b>Package maintainer</b>: ${ c.package.maintainer }</li>
    % if c.package.unapproved_screenshots.count()>0:
        <li>
            <em>
            ${ c.package.unapproved_screenshots.count() } new screenshots are
            waiting for approval by the admin team.
            </em>
        </li>
    % endif
    <li><a href="http://packages.debian.org/${ c.package.name }" target="_blank">Package
        page on packages.debian.org</a></li>
</ul>
</div>

## Show approved screenshots
<div class="screenshots">
<h1>Available screenshots</h1>
<p><i>
    (These screenshots are licensed under the same terms as
    '${ c.package.name }' itself.)
</i></p>
% if c.package.approved_screenshots.count():
% for screenshot in c.package.approved_screenshots:
    <div class="screenshot">
    <a class="image" href="${h.url_for('image', id=screenshot.large_image.id)}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${h.url_for('image', id=screenshot.small_image.id)}" alt="Screenshot" />
    </a>
    <br />
    ## TODO: Fancy icons :)
    ## Display a message if the screenshot is markedfordelete
    % if screenshot.markedfordelete:
        (Removal was requested.)
    % else:
        ## Admins can remove the screenshots directly:
        % if ('username' in session) or (h.my.client_cookie_hash() == screenshot.uploaderhash):
            ${ h.tags.link_to(
                'Remove this screenshot',
                h.url_for('delete_screenshot', screenshot=screenshot.id),
                onclick=h.tags.literal('return confirm(\'Really delete this screenshot?\')')) }
        ## Visitors can mark this package for deletion:
        % else:
            ${ h.tags.link_to(
                'Request removal',
                '#',
                id='markfordelete',
                ) }
            ## Hidden field to enter the reason for markedfordelete
            <div id="markfordelete-form" style="display: none">
                ${ h.tags.form(h.url_for('delete_screenshot', screenshot=screenshot.id))}
                Why should it get removed?
                <br />
                ${ h.tags.text('reason', id='markfordelete-reason') }
                <br />
                ${ h.tags.submit('submit', 'Okay') }
                </form>
            </div>
        % endif
    % endif
    </div>
% endfor
% else:
<p>There are no approved screenshots for this package yet.</p>
% endif
</div>

## Show screenshots that are not yet approved but uploaded by the
## current visitor (identified by their client cookie hash value).
## This view is not shown if the user is an administrator or otherwise
## the screenshots would also show up in the "not yet approved screenshots"
## section below.
% if ('username' not in session) and (c.package.my_screenshots.count()):
<div class="screenshots">
<h1>Your uploaded (not yet approved) screenshots</h1>
% for screenshot in c.package.my_screenshots:
    <div class="screenshot">
    <a class="image" href="${h.url_for('image', id=screenshot.large_image.id)}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${h.url_for('image', id=screenshot.small_image.id)}" alt="Screenshot" />
    </a>
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
% if 'username' in session and c.package.unapproved_screenshots.count():
<div class="screenshots">
<h1>Not yet approved screenshots</h1>
% for screenshot in c.package.unapproved_screenshots:
    <div class="screenshot">
    <a class="image" href="${h.url_for('image', id=screenshot.large_image.id)}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${h.url_for('image', id=screenshot.small_image.id)}" alt="Screenshot" />
    </a>
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
