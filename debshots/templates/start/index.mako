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

## Function to show debtags for a certain facet
function showtags(tagid) {
    var content = $('#debtags-'+tagid).html();
    $('#tags-box').fadeOut('fast', function () {
        $('#tags-box').html(content);
        $('#tags-box').fadeIn('fast');
    });
    ## Mark the facet as selected
    $('.frontpage-facet').removeClass('selected');
    $('#facet-'+tagid).addClass('selected');
}
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
            ## Link to package's page
            <a href="${ h.url('package', package=pkg.name) }">
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
            </a>
        </div>
    % endfor
    </div>
</div>
% endif

## Top-right: Teaser and search box
<div id="teaser-search" style="margin-left: 400px;">
    <div style="text-align: center">
        <h1 class="huge">
            ${c.number_of_screenshots} screenshots online.<br />
            Like to ${ h.tags.link_to('add one', h.url('upload')) }, too?
        </h1>

        <h1>Search for a package/description:</h1>
        ${ h.tags.form('packages') }
            <div>
                ${ h.tags.text('search') }
            </div>
        </form>
    </div>
</div>

<h1>Or browse by debtags:</h1>

<div id="debtags-area">
    <div id="debtags-facets">
        % for i,facet in enumerate(sorted(c.facets_and_tags)):
        <div id="facet-${i}" class="frontpage-facet" onclick="showtags(${i})">${ facet }</div>
        % endfor
    </div>

    <div id="tags-box">
    </div>

    % for i,facet in enumerate(sorted(c.facets_and_tags)):
    <div id="debtags-${i}" style="display: none">
        % for tag in sorted(c.facets_and_tags[facet]['tags']):
            <div>
                <a href="${h.url('packages', debtag=tag.tag)}">${ tag.description.splitlines()[0] }</a>
            </div>
        % endfor
    </div>
    % endfor
<br style="clear: both" />
</div>
