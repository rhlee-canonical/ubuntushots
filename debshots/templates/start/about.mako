# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<h1>About this site</h1>

<p>
    This is a public repository of screenshots taken from applications contained in the Debian
    GNU/Linux distribution and its derivates like Ubuntu. It was created to help getting an
    impression of what a certain software will look like on your desktop before you install it.
    Everybody can take screenshots and upload them. Our admin team will just review your
    changes before they become publicly visible.
</p>

<h1>Which packages are listed?</h1>

<p>
    The information on packages listed on this site is taken from APT repositories
    like Debian or Ubuntu. We are just throwing out packages that are bad candidates
    for screenshots like transitional packages, header files or debug packages.
    The repositories that we are scanning frequently are:
    <ul>
    % for repository in c.repositories:
        <li>${ repository }</li>
    % endfor
    </ul>
</p>

<h1>Who is using this site?</h1>

<p>
    Many users of Debian or Ubuntu visit this site to just browse through the
    huge pool of packages visually. It is obviously much easier to just look at
    screenshots than install various packages just to try them out.
    And other users are not even aware they are using this site. This is because
    tools like "Synaptic" or Ubuntu's "Software Center" are loading screenshots from here.
</p>

<h1>How you can use the screenshots</h1>

<p>
    You can use the screenshots on your own website. Some useful URLs:
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
    <li>
        http://screenshots.debian.net/rss
        <br />
        (An RSS feed showing the most recently uploaded screenshots.)
    </li>
</ul>

<p>
    If you would like to get a complete list of packages or screenshots in JSON format
    then contact us and we will give you the URL.
</p>

<h1>Uploading new screenshots</h1>

<p>
    Whether you are a developer or not - we appreciate if you upload screenshots.
    See if your favorite package does not yet have a screenshot and upload one.
</p>

<h1>Statistics</h1>

<p>
    We currently have ${ c.packages_count } packages in our database.
    ${ c.packages_with_screenshots_count } of them have screenshots.
    That makes a total of ${ round(c.screenshots_percentage, 1) }%.
    We have ${ c.screenshots_count } screenshots on the server which means
    every package has an average number of ${ round(c.average_screenshots_per_package,1) }
    screenshots.
</p>

## Display screenshots graph using Google Chart API
<p>
    <img src="${ c.chart_url}" />
    <div>(<i>Number of screenshots online each month.)</i></div>
</p>

<h1>Who is behind this site?</h1>

<p>
    This site has been developed and is maintained by
    <a href="mailto:email@christoph-haas.de">Christoph Haas</a>.
    In order to be able to publish newly uploaded screenshots in time several
    more people are moderating uploads:
</p>

<ul>
    <li>Dean Sutherland</li>
    <li>Paul Wise</li>
    <li>Martin Stigge</li>
    <li>J. Richards</li>
</ul>

<h1>This web site's software</h1>

<p>
    This site runs on <em>debshots</em> - a <a href="http://pylonshq.com/">Pylons</a>-based web
    application written by <a href="mailto:email@christoph-haas.de">Christoph Haas</a>.
    <em>debshots</em> also uses <a href="http://www.sqlalchemy.org/">SQLAlchemy</a> for
    accesing its <a href="http://www.postgresql.org/">PostgreSQL</a> database, the <a
    href="http://jquery.com">jQuery</a> Javascript library and its <a
    href="http://nixboxdesigns.com/demos/jquery-image-flyout.php">flyout</a>, <a
    href="http://bassistance.de/jquery-plugins/jquery-plugin-autocomplete/">autocomplete</a>,
    <a href="http://stanlemon.net/projects/jgrowl.html">jGrowl</a> and <a
    href="http://malsup.com/jquery/cycle/">cycle</a> plugins. Further code has been
    contributed by Michael Vogt - programmer of Synaptic and Ubuntu's
    <em>Software Center</em>.
</p>

<p>
    If you are interested in looking at its source code then check out its development home
    page listing known issues and desired features at <a
    href="http://debshots.workaround.org/">debshots.workaround.org</a>. The software is still
    actively developed and improved.
</p>
