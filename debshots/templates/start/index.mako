# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<script type="application/x-javascript">
$(document).ready(function() {
    $('#rotated').cycle({
		fx: 'fade',
                timeout: ${ c.gallery_switch_time }
	});

    $('input#searchterm').focus();
});
</script>

## Activate Lightbox plugin for screenshots DIV
<%include file="/packages/include-js-flyout.mako"/>

## Top-left: slideshow of new uploads
% if c.newest_screenshots:
<div id="new-uploads" style="float: left">
<h1>Latest uploads...</h1>
 <div id="rotated" style="width: 350px; height: 130px">
    % for pkg in c.packages_with_newest_screenshots:
        <% screenshot = pkg.screenshots[0] %>
        <div>
            ## TODO: add link to package details page
            <table><tr>
                <td class="noborder">
                    ${ h.tags.image(screenshot.small_image_url, alt='Screenshot of package %s' % pkg.name) }
                </td>
                <td class="noborder">
                    <div>
                        <b>${ pkg.name }</b>
                    </div>
                    <p>
                        ${ pkg.description }
                    </p>
                </td>
            </tr></table>
        </div>
    % endfor
    </div>
</div>
% endif

## Top-right: Teaser and search box
<div id="teaser-search" style="margin-left: 400px;">
    <div style="text-align: center">
    <h1 style="font-size: 300%;">
        ${c.number_of_screenshots} screenshots online.<br>
        Like to add one, too?
    </h1>

    <h1>Search for a package/description:</h1>
    ${ h.tags.form('search') }
        ${ h.tags.text('searchterm') }
    </form>
    </div>
</div>

## Center: debtags
<div id="tagtable">
    <h1>Browse the packages by category:</h1>
    <table>
        <tr>
            <td>
                <em>Accessibility support</em><br>
                Input Systems, Text Recognition, Screen Magnification,
                Screen Helper, Some other category
            </td>
            <td>
                <em>Accessibility support</em><br>
                Input Systems, Text Recognition, Screen Magnification,
                Screen Helper, Some other category
            </td>
            <td>
                <em>Accessibility support</em><br>
                Input Systems, Text Recognition, Screen Magnification,
                Screen Helper, Some other category
            </td>
        </tr>
        <tr>
            <td>
                <em>Accessibility support</em><br>
                Input Systems, Text Recognition, Screen Magnification,
                Screen Helper, Some other category
            </td>
            <td>
                <em>Accessibility support</em><br>
                Input Systems, Text Recognition, Screen Magnification,
                Screen Helper, Some other category
            </td>
            <td>
                <em>Accessibility support</em><br>
                Input Systems, Text Recognition, Screen Magnification,
                Screen Helper, Some other category
            </td>
        </tr>
        <tr>
            <td>
                <em>Accessibility support</em><br>
                Input Systems, Text Recognition, Screen Magnification,
                Screen Helper, Some other category
            </td>
            <td>
                <em>Accessibility support</em><br>
                Input Systems, Text Recognition, Screen Magnification,
                Screen Helper, Some other category
            </td>
            <td>
                <em>Accessibility support</em><br>
                Input Systems, Text Recognition, Screen Magnification,
                Screen Helper, Some other category
            </td>
        </tr>
    </table>
</div>
