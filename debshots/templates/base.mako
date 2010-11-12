# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>
        screenshots.debian.net
        % if c.title:
        - ${c.title}
        % endif
    </title>
    ${ h.tags.stylesheet_link(
        '/css/style.css',
        ) }
    ${ h.tags.javascript_link(
        '/javascript/jquery.js',
        '/javascript/jquery.autocomplete.js', ## for data entry
        '/javascript/jquery.flyout.js', ## for image zooming
        '/javascript/jquery.jgrowl.js', ## message popup balloons
        '/javascript/jquery.tooltip.js', ## tooltip popups (for facets descriptions)
        '/javascript/jquery.cycle.js', ## new uploads slideshow on the front page
        '/javascript/handlers.js', ## new uploads slideshow on the front page
        ) }
    <link rel="alternate" href="/rss" title="RSS Feed" type="application/rss+xml" />

    ## display popup messages stored in the session via jGrowl (jQuery plugin)
    % if session.get('messages'):
        % for message in session['messages'].pop():
        <script type="application/x-javascript">
            $(document).ready(function() {
                $.jGrowl('${h.tags.literal(message)}');
            });
        </script>
        % endfor
        <% session.save() %>
    % endif

    ## Favicon
    <link rel="shortcut icon" type="image/x-icon" href="/favicon.png" />
  </head>

  <body>
    <div id="page">
      <div id="header">
        <ul>
          <li>
            <a href="/">Home</a>
          </li>
          <li>
            <a href="/packages">Browse screenshots</a>
          </li>
          <li>
            <a href="/upload">Upload screenshots</a>
          </li>
        </ul>
        <img src="/images/logo.png" alt="screenshots.debian.net" />
      </div>

      <div id="maincontent">
      ${ next.body() }
      </div>
    </div>
    ## end of #page

    <div id="footer">
        ${ h.tags.link_to('About screenshots.debian.net', h.url('about')) }
        ## TODO: The start page gets cached so the "logged in" appears to the wrong people
        ##% if 'username' in session:
        ##<p style="color: red">
        ##You're logged in as <em>${session['username']}</em>.
        ##<a href="/logout">(Logout)</a>
        ##</p>
        ##% endif
    </div>

    ## Google analytics
    % if 'debshots.google_analytics_id' in config:
    <script type="text/javascript">
        var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
        document.write(unescape("%3Cscript src='" + gaJsHost +
        "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
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
