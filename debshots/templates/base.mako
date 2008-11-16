# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>screenshots.debian.net</title>
    ${ h.tags.stylesheet_link(
        '/css/style.css',
        ) }
    ${ h.tags.javascript_link(
        '/javascript/jquery.js',
        '/javascript/jquery.autocomplete.js', ## for data entry
        '/javascript/jquery.flyout.js', ## for image zooming
        '/javascript/jquery.jgrowl.js', ## message popups
        ) }
    <!--<link rel="alternate" href="some feed url" title="RSS Feed" type="application/rss+xml" />-->

    ## display popup messages stored in the session via jGrowl (jQuery plugin)
    % if session['messages']:
        % for message in session['messages'].pop():
        <script type="application/x-javascript">
            $(document).ready(function() {
                $.jGrowl('${ message }');
            });
        </script>
        % endfor
        <% session.save() %>
    % endif
  </head>

  <body>
    <div id="header">
        <img src="/images/logo.png" alt="screenshots.debian.net" />
    </div>

    <div id="nav">
        <a href="/">Home</a>
        |
        <a href="/packages">Browse screenshots</a>
        |
        <a href="/upload">Upload screenshots</a>
        |
        <a href="/guidelines">Screenshot guidelines</a>
    </div>

    <div id="maincontent">
${ next.body() }
    </div>

    <div id="footer">
        Powered by
        <a href="mailto:haas@debian.org">Christoph Haas'</a>
        <a href="http://hg.workaround.org/repositories/debshots/">debshots</a> software
        using the <a href="http://pylonshq.com">Pylons web framework</a>
        and <a href="http://jquery.com">jQuery Javascript framework</a>.
        % if 'username' in session:
        Logged in as <em>${session['username']}</em>.
        <a href="/logout">(Logout)</a>
        % endif
    </div>

    ## Google analytics
    % if 'debshots.google_analytics_id' in config:
    <script type="text/javascript">
        var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl.
    " : "http://www.");
        document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics
    .com/ga.js' type='text/javascript'%3E%3C/script%3E"));
    </script>
    <script type="text/javascript">
        try {
        var pageTracker = _gat._getTracker("${ config['debshots.google_analytics_id'] }");
        pageTracker._trackPageview();
        } catch(err) {}
    </script>
    % endif
  </body>
</html>
