# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-js-autocomplete-package.mako"/>

<script type="application/x-javascript">
    $(document).ready(function() {
        $('#autocompletehint').html('(just type the first letters)');

        $('#packagename').change(packagename_changed);

        ## The /upload action allows to specify an optional package
        % if c.packagename:
            $('#packagename').val('${c.packagename}')
            packagename_changed();
        % endif
    });

    function packagename_changed () {
        // Get the current package version from the database
        package = $('#packagename').val();

        // Fetch the version number from the database
        $.getJSON(
            '/packages/ajax_get_version_for_package',
            { q: package },
            function (data) {
                // Insert the version number into the respective field
                $('#version').val(data.version);
                }
            )
        }
</script>


<h1>Upload screenshots</h1>

<p>Please enter the name of the package you wish to upload a screenshot for:</p>

${ h.tags.form(h.url_for('uploadfile'), method='post', multipart=True) }
<table>
<tr>
    <td>Package name:</td>
    <td>
        <input type="text" name="packagename" id="packagename" size="40" />
        <span id="autocompletehint"></span>
    </td>
</tr>
<tr>
    <td>Software version:</td>
    <td>
        <input type="text" name="version" id="version" size="40" /> (optional)
    </td>
</tr>
<tr>
    <td>Screenshot (PNG file):</td>
    <td>
        <input type="file" name="file" size="40"/>
    </td>
</tr>
</table>
<input type="submit" value="Upload screenshot" />
</form>

% if c.message:
<p class="error-message">${ c.message }</p>
% endif

<h1>Guidelines for taking screenshots</h1>

<ul>
    <li>Screenshots are published under the terms of the packaged software itself.</li>
    <li>Your screenshots must be in PNG format.</li>
    <li>Due to legal reasons screenshots for non-free packages aren't accecpted.</li>
    <li>Images larger than 800x600 pixels will automatically be reduced to that
        size (retaining the aspect ratio of course).
        So if you like to control the exact result of what you upload then
        make sure your image size is no larger than that.</li>
    <li>Your screenshot should contain a typical scene when working with it.
        When snapshotting a browser load the debian.org home page. A screenshot
        of a graphics program should have a drawing loaded. Of a game please make
        a screenshot while you are playing and not of the start screen.
    </li>
    <li>
        Nice tools for taking screenshots are shutter, ksnapshot (KDE), gimp, xwd or scrot.
        See the <a href="http://wiki.debian.org/ScreenShots">Debian wiki</a> for more information
        on how to make screenshots under Debian.
    </li>
    <li>You need not artificially switch off your window decorations.</li>
    <li>
        Please set your language to english so that everybody understands it.
        If you don't use english by default please start your application
        from a shell using after setting "export LANG=C".
    </li>
    <li>
        Please only take a screenshot of the respective application and not
        of your whole desktop (unless the screenshot is meant for a
        window manager).
    </li>
    <li>
        Interlaced PNG files cannot be processed currently.
        Please use non-interlaced images.
    </li>
</ul>

<p>Remember: your uploaded screenshot will not be visible immediately. It will first
be checked by the admin team. It is already visible to you though.</p>

