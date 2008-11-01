# -*- coding: utf-8 -*-
## Details and screenshots of a package
<%inherit file="/base.mako"/>

<div class="graybox">
<h1>Screenshots for package <em>'${ c.package.name }'</em></h1>
<ul>
    <li>Description: ${ c.package.cachebinarypackage.description }</li>
    <li>Section: ${ c.package.cachebinarypackage.section }</li>
    % if c.package.cachebinarypackage.homepage:
        <li>Section: ${ c.package.cachebinarypackage.homepage }</li>
    % endif
    <li>Package maintainer: ${ c.package.cachebinarypackage.maintainer }</li>
</ul>
</div>

<div>
% if c.package.small_screenshots:
% for screenshot in c.package.small_screenshots:
    ${ h.tags.image(h.url_for('image', id=screenshot.id), alt='Screenshot') }
% endfor
## TODO: pager
% else:
<p>There are no screenshots for this package yet.</p>
% endif
</div>