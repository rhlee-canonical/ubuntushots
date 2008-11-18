# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<h1>How does this website work?</h1>
<p>
    This is a public repository of screenshots taken from applications contained in the Debian
    GNU/Linux distribution. It was created to help getting an impression of what a certain
    software will look like on your desktop before you install it. Everybody can take
    screenshots and upload them. Our admin team will just review your changes before they become
    publicly visible.
</p>

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
            h.url_for('package', package=screenshot.package.name)) }
    </div>
    % endfor
    </div>
    <br clear="all" />
% endif

<h1>Uploading new screenshots</h1>
<p>
    Whether you are a developer or not - we appreciate if you upload screenshots. Please take
    a look at the <a href="/guidelines">guidelines</a>
    for taking screenshots. Then see if your favorite package does not yet have a screenshot
    and upload one.
</p>

<h1>Browsing screenshots</h1>
<p>
    Are you looking for a certain piece of software? Browse our repository by searching for a
    program name or a search word.
</p>

<h1>Software supporting screenshots</h1>
<p>
    Michael Vogt has added support into <em>synaptic</em>.
</p>

<h1>Using our screenshots</h1>
<p>
    You can use the screenshots on your own website. These are the URLs that may be useful:
</p>

<ul>
    <li>
        http://screenshots.debian.net/packages
        <br />
        (List of all packages with screenshots)
    </li>
    <li>
        http://screenshots.debian.net/package/PACKAGENAME
        <br />
        (Page with details and screenshots for a certain package)
    </li>
    <li>
        http://screenshots.debian.net/thumbnail/PACKAGENAME
        <br />
        (Returns a thumbnail (160x120 pixels or less) of a package's first found
        screenshot. If no screenshot was found then a dummy image will be returned.
        In no case an HTTP error 404 is returned.)
    </li>
    <li>
        http://screenshots.debian.net/screenshot/PACKAGENAME
        <br />
        (Returns a screenshot (800x600 pixels or less) of a package.
        If no screenshot was found then a dummy image will be returned.
        In no case an HTTP error 404 is returned.)
    </li>
</ul>
