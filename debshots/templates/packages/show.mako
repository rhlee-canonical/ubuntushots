# -*- coding: utf-8 -*-
## Details and screenshots of a package

<%inherit file="/base.mako"/>

<script type="application/x-javascript">
$(document).ready(function() {
    inithandlers();
});
</script>

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
    % if c.package.origin:
	<li><b>Origin</b>: ${ c.package.origin }</li>
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
    <li>${ h.package_page_link(c.package) }</li>
    <li>${ h.bugs_page_link(c.package) }</li>
    ## Upload link:
    <li>${ h.tags.link_to('Upload a new screenshot',
            h.url('upload', package=c.package.name)) }</li>
</ul>

</td><td class="noborder">

## Debtags
% if c.package.debtags:
    <h2>Tags
	<img src="/icons/help.png" title="Debtags are an invention of Enrico Zini to
	help classify Debian packages. See debtags.alioth.debian.org" class="tooltip"
	alt="Tooltip" />
    </h2>
    <ul>
    % for facet, facet_data in c.package.tags_grouped_by_facet.iteritems():
        <li>
	    <span class="facet">
            % if facet_data['description_long']:
                <span class="tooltip" title="${ facet_data['description_long'] }">${ facet_data['description_short'] }</span>
	    % else:
		${ facet_data['description_short'] }
            % endif
	    </span>
	    &rarr;
	    ## Show all tags of this facet
	    % for tag in facet_data['tags']:
		<span class="debtag">
		## If the tag has a long description then add it as a tooltip
		% if tag.description_long:
		    <a class="tooltip" title="${ tag.description_long }" href="${ h.url('packages', debtag=tag.tag) }">
		    ${ tag.description_short }
		    </a>
		% else:
		    <a href="${ h.url('packages', debtag=tag.tag) }">
		    ${ tag.description_short }
		    </a>
		% endif
		</span>
	    % endfor
        </li>
    % endfor
    </ul>
% endif
</td></tr></table>
</div>

## Show approved screenshots
<div>
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
	% if screenshot.description:
	<br />
	<i>${ screenshot.description }</i>
	% endif
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
                h.url('delete_screenshot', screenshot=screenshot.id),
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
                ${ h.tags.form(h.url('delete_screenshot', screenshot=screenshot.id))}
                <p>Why should it get removed?
                <br />
                ${ h.tags.text('reason', size=20, maxlength=100) }
                <br />
                ${ h.tags.submit('submit', 'Okay') }
		</p>
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
    % if screenshot.description:
    <br />
    <i>${ screenshot.description }</i>
    % endif
    % if screenshot.version:
    <br />
    Version: ${ screenshot.version }
    % endif
    ## Allow the visitor to delete their own screenshots
    <br />
    ## TODO: Fancy icons :)
    ${ h.tags.link_to(
        'Delete your screenshot',
        h.url('delete_screenshot', screenshot=screenshot.id),
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
    % if screenshot.description:
    <br />
    <i>${ screenshot.description }</i>
    % endif
    % if screenshot.version:
    <br />
    Version: ${ screenshot.version }
    % endif
    ## Allow the visitor to delete their own screenshots
    <br />
    ## TODO: Fancy icons :)
    ${ h.tags.link_to(
        'Approve screenshot',
        h.url('approve_screenshot', screenshot=screenshot.id, goto=h.url())) }
    <br />
    ${ h.tags.link_to(
        'Delete screenshot',
        h.url('delete_screenshot', screenshot=screenshot.id, goto=h.url()),
        onclick=h.tags.literal('return confirm(\'Really delete this screenshot?\')')) }
    </div>
% endfor
</div>
% endif
