# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<script type="application/x-javascript">
$(document).ready(function() {
    $('#rotated').cycle({
		fx: 'fade',
                timeout: ${ c.gallery_switch_time }
	});

    $('.facet').hover(function() {
        $(this).find('div.tags').show();
    }, function() {
        $(this).find('div.tags').hide();
    });

    $('#accordion-1').easyAccordion({
        slideNum: false
                    //autoStart: true
                    //slideInterval: 3000
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
##</pre>
<div id="tagtable">
    <h1>Browse the packages by category:</h1>
    <div id="accordion-1">
    <dl>
        % for facet_counter,facet in enumerate(c.facets_and_tags):
                <dt>${facet}</dt>
                <dd>
                    % for tag in c.facets_and_tags[facet]['tags']:
                        ${ tag.description_short },
                    % endfor
                </dd>
        % endfor
    </dl>
    </div>
</div>



        <div id="accordion-2">

            <dl>
                <dt>First slide</dt>
                <dd><h2>This is the first slide</h2><p><img src="images/monsters/img1.png" alt="Alt text to go here" />Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, enim.<br /><a href="#" class="more">Read more</a></p></dd>
                <dt>Second slide</dt>
                <dd><h2>Here is the second slide</h2><p><img src="images/monsters/img2.png" alt="Alt text to go here" />Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, enim.<br /><a href="#" class="more">Read more</a></p></dd>

                <dt>One more slide</dt>
                <dd><h2>One more slide to go here</h2><p><img src="images/monsters/img3.png" alt="Alt text to go here" />Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, enim.<br /><a href="#" class="more">Read more</a></p></dd>
                <dt>Another slide</dt>
                <dd><h2>Another slide to go here</h2><p><img src="images/monsters/img4.png" alt="Alt text to go here" />Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, enim.<br /><a href="#" class="more">Read more</a></p></dd>
                <dt>Wow one more</dt>

                <dd><h2>Unbilievable one more slide here</h2><p><img src="images/monsters/img5.png" alt="Alt text to go here" />Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, enim.<br /><a href="#" class="more">Read more</a></p></dd>
                <dt>Last one</dt>
                <dd><h2>This is definitely the last one</h2><p><img src="images/monsters/img6.png" alt="Alt text to go here" />Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, enim.<br /><a href="#" class="more">Read more</a></p></dd>
            </dl>
        </div>
