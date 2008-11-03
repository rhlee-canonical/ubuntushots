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
        '/javascript/jquery.autocomplete.js',
        '/javascript/jquery.flyout.js',
        ) }
    <!--<link rel="alternate" href="some feed url" title="RSS Feed" type="application/rss+xml" />-->
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
        ## Admin options:
        % if 'username' in session:
        |
        <a href="/logout">Logout</a>
        % endif
    </div>

    <div id="maincontent">
${ next.body() }
    </div>

    <div id="footer">
        Powered by Christoph Haas' <em>debshots</em> software.
        % if 'username' in session:
        Logged in as <em>${session['username']}</em>.
        % endif
    </div>

  </body>
</html>
