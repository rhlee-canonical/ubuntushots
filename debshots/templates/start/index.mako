# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<script type="application/x-javascript">
$(document).ready(function() {
    $('#rotated').cycle({
		fx: 'fade',
                timeout: ${ c.gallery_switch_time }
	});

    ## Display facets of a tag in the middle column upon clicking on a tag
    //$('#tags-left div').click(function() {
    //    ## Get the facet that was clicked
    //    facet=$(this).html();
    //
    //    ## AJAH-load the appropriate tags into the center column
    //    $('#tags-center').load('/ajah/facet2tags', { 'facet':facet }, middle_column_magic);
    //});

    ## Fill a Javascript with facets and debtags
##    facets = new Array();
##    tags = new Array();
##    % for i,facet in enumerate(sorted(c.facets_and_tags)):
##        facets[${i}]="${facet}";
##        tags[${i}]=new Array;
##        % for j,tag in enumerate(sorted(c.facets_and_tags[facet]['tags'])):
##            tags[${i}][${j}]="${tag.description.splitlines()[0]}";
##        % endfor
##    % endfor

    $('#debtags-facets span').click( function() {
        var div_to_show = '#debtags-'+$(this).attr('id');
        var content = $(div_to_show).html();
        $('#tags-box').fadeOut('fast', function ()  {
            $('#tags-box').html(content);
            $('#tags-box').fadeIn('fast');
        });
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
        Like to ${ h.tags.link_to('add one', h.url('upload')) }, too?
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

<div id="debtags-area">
    <div id="debtags-facets" class="tags-box">
        % for i,facet in enumerate(sorted(c.facets_and_tags)):
            <span id="facet-${i}">${ facet }</span>
        % endfor
    </div>

    <div id="tags-box" class="tags-box">
    </div>

    % for i,facet in enumerate(sorted(c.facets_and_tags)):
    <div id="debtags-facet-${i}" style="display: none">
        % for tag in c.facets_and_tags[facet]['tags']:
            <span>${ tag.description.splitlines()[0] }</span>
        % endfor
    </div>
    % endfor
</div>

<br clear="all" />
