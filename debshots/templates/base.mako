# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
  <head>
    <title>screenshots.debian.net</title>
    ${ h.tags.stylesheet_link('/css/style.css') }
    ${ h.tags.javascript_link(
        '/javascript/jquery.js',
        '/javascript/jquery.autocomplete.js'
        ) }
    <!--<link rel="alternate" href=" c.feed_url " title="RSS Feed" type="application/rss+xml" />-->
  </head>

  <body>
    <div id="header">
      <!--<div id="headertitle">-->
        <img src="/images/logo.png" alt="screenshots.debian.net" />
      <!--</div>-->
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

  </body>
</html>
