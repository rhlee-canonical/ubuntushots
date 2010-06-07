# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

% if c.newest_screenshots:
## Activate Lightbox plugin for screenshots DIV
<%include file="/packages/include-js-lightbox.mako"/>
<h1>Newest screenshots</h1>
    <div class="screenshots">
    % for screenshot in c.newest_screenshots:
    <div class="screenshot" style="height: 150px">
    <a class="image" href="${screenshot.large_image_url}"
        title="Screenshot of package '${screenshot.package.name}'">
        <img src="${screenshot.small_image_url}" alt="Screenshot" />
    </a>
    <br />
        ${ h.tags.link_to(
            screenshot.package.name,
            h.url('package', package=screenshot.package.name)) }
    </div>
    % endfor
    </div>
    <br clear="all" />
% endif

<h1>Browsing screenshots</h1>
<p>
    Are you looking for a certain piece of software? Browse our repository by searching for a
    program name or a search word.
</p>

