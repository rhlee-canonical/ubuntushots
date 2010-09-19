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
##<pre>
##    % for facet in c.facets_and_tags:
##        Facet: ${facet} (${c.facets_and_tags[facet]['facet']})
##        % for tag in c.facets_and_tags[facet]['tags']:
##            - ${ tag.description_short } (${tag.tag})
##        % endfor
##    % endfor
</pre>
<div id="tagtable">
    <h1>Browse the packages by category:</h1>
    <table>
        <tr>
        % for facet_counter,facet in enumerate(c.facets_and_tags):
            <td>
                <em>${facet}</em><br />
                % for tag in c.facets_and_tags[facet]['tags']:
                ${ tag.description_short },
                % endfor
            </td>
            % if facet_counter % 4 == 3:
                </tr>
                <tr>
            % endif
        % endfor
        </tr>
    </table>
</div>
