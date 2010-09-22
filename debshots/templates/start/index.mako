# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<script type="application/x-javascript">
$(document).ready(function() {
    $('#rotated').cycle({
		fx: 'fade',
                timeout: ${ c.gallery_switch_time }
	});

    ## Mouse-over effect on the left facets column
    $('#tags-left div').hover(function() {
        $(this).addClass('tag-highlighted');
    }, function() {
        $(this).removeClass('tag-highlighted');
    });

    ## Display facets of a tag in the middle column upon clicking on a tag
    $('#tags-left div').click(function() {
        ## Get the facet that was clicked
        facet=$(this).html();

        ## AJAH-load the appropriate tags into the center column
        $('#tags-center').load('/ajah/facet2tags', { 'facet':facet }, middle_column_magic);
    });

    $('input#searchterm').focus();
});

function middle_column_magic() {
    ## Mouse-over effect on the center tags column
    $('#tags-center div').hover(function() {
        $(this).addClass('tag-highlighted');
    }, function() {
        $(this).removeClass('tag-highlighted');
    });
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
    <h1 style="font-size: 200%;">
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
##<pre>
##    % for facet in c.facets_and_tags:
##        Facet: ${facet} (${c.facets_and_tags[facet]['facet']})
##        % for tag in c.facets_and_tags[facet]['tags']:
##            - ${ tag.description_short } (${tag.tag})
##        % endfor
##    % endfor
##</pre>

##<div id="tagtable">
##    <h1>Browse the packages by category:</h1>
##    <div id="accordion-1">
##    <dl>
##        % for facet_counter,facet in enumerate(c.facets_and_tags):
##                <dt>${facet}</dt>
##                <dd>
##                    % for tag in c.facets_and_tags[facet]['tags']:
##                        ${ tag.description_short },
##                    % endfor
##                </dd>
##        % endfor
##    </dl>
##    </div>
##</div>

<div id="tags-left" class="tags-box">
    % for facet in sorted(c.facets_and_tags):
        <div>${ facet }</div>
    % endfor
</div>

<div id="tags-center" class="tags-box">
    Select a category on the left
##    <ul>
##
##        ${ c.facets_and_tags['Role']['tags'][0].description }
##        <li>text</li>
##    </ul>
</div>

<div id="tags-right" class="tags-box">
    rechts
</div>

<br clear="all" />
