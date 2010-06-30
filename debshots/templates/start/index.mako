# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

##% if c.newest_screenshots:
## Activate Lightbox plugin for screenshots DIV
<%include file="/packages/include-js-flyout.mako"/>
##<h1>Newest screenshots</h1>
##    <div class="screenshots">
##    % for screenshot in c.newest_screenshots:
##    <div class="screenshot" style="height: 150px">
##    <a class="image" href="${screenshot.large_image_url}"
##        title="Screenshot of package '${screenshot.package.name}'">
##        <img src="${screenshot.small_image_url}" alt="Screenshot" />
##    </a>
##    <br />
##        ${ h.tags.link_to(
##            screenshot.package.name,
##            h.url('package', package=screenshot.package.name)) }
##    </div>
##    % endfor
##    </div>
##    <br clear="all" />
##% endif

% if c.newest_screenshots:
    <h1>Latest uploads</h1>

    % for pkg in c.packages_with_newest_screenshots:
    <% screenshot = pkg.screenshots[0] %>
    <div style="">
        ## Thumbnail
        <td class="noborder">
            <a class="image" href="${screenshot.large_image_url}"
            title="Screenshot of package '${screenshot.package.name}'">
            <img src="${ screenshot.small_image_url }" alt="Screenshot" />
            </a>
    </div>
    <div style="">
        ## Name (click->details page) + more info
            <p class="namelink">
                ${ h.tags.link_to(pkg.name, h.url('package', package=pkg.name)) }
            </p>
            <p>${ pkg.description }</p>
            <p><i>(Section: ${ pkg.section }
                % if pkg.origin:
                    /
                    Origin: ${ pkg.origin }
                % endif
                )
                </i>
            </p>
    </div>
    % endfor
% endif
