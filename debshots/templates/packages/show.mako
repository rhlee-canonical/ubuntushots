# -*- coding: utf-8 -*-
## Details and screenshots of a package
<%inherit file="/base.mako"/>

<script type="application/x-javascript">
    $(document).ready(function() {
        ## Flyout shows the large screenshots when clicking on the thumbnails
        $('.screenshots a').flyout({
            loadingSrc:'/images/spinner.gif',
            outSpeed: 300,
            inSpeed: 300
        });
    });
</script>

<div class="graybox">
<h1>Package <em>'${ c.package.name }'</em></h1>
<ul>
    <li>Description: ${ c.package.cachebinarypackage.description }</li>
    <li>Section: ${ c.package.cachebinarypackage.section }</li>
    % if c.package.cachebinarypackage.homepage:
        <li>Homepage: ${ c.package.cachebinarypackage.homepage }</li>
    % endif
    <li>Package maintainer: ${ c.package.cachebinarypackage.maintainer }</li>
    % if c.package.uploaded_screenshots.count()>0:
        <li>
            ${ c.package.uploaded_screenshots.count() } new screenshots are
            waiting for approval by the admin team.
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
    </div>
% endfor
% else:
<p>There are no approved screenshots for this package yet.</p>
% endif
</div>

## Show screenshots that are not yet approved but uploaded by the
## current user (identified by their client cookie hash value)
<div class="screenshots">
% if c.package.my_screenshots.count():
<h1>Your uploaded screenshots</h1>
% for screenshot in c.package.my_screenshots:
    <div class="screenshot">
    <a class="image" href="${h.url_for('image', id=screenshot.large_image.id)}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${h.url_for('image', id=screenshot.small_image.id)}" alt="Screenshot" />
    </a>
    </div>
% endfor
% endif
</div>
