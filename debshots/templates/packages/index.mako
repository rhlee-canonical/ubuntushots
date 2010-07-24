# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-index-header.mako"/>
<%include file="/packages/include-js-flyout.mako"/>

% if c.packages:
    <% pager = c.packages.pager('Page: $link_previous $link_next ~10~') %>
    <ul class="quicksand">
    <p>${ pager}</p>
    % for package in c.packages:
    <li data-id="pkg-${ package.id }">
        <!--<i>${ package.description }</i>-->
        <!--${ package.section }-->
        <!--## Show link to upload screenshots-->
        <!--${ h.tags.link_to('Upload a screenshot', h.url('upload', package=package.name)) }-->
        ## Second line shows screenshots
        <% my_or_approved_screenshots = package.my_or_approved_screenshots %>
        % if my_or_approved_screenshots:
            <div class="screenshots">
##            % for screenshot in my_or_approved_screenshots:
                <% screenshot = my_or_approved_screenshots[0] %>
                <a class="image" href="${screenshot.large_image_url}"
                    title="Screenshot of package '${screenshot.package.name}'">
                    <img src="${screenshot.small_image_url}" alt="Screenshot" />
                </a>
##            % endfor
            </div>
            <div class="textcenter">
                ${ h.tags.link_to(package.name, h.url('package', package=package.name)) }
            </div>
        % else:
            ## Show dummy screenshot
            ${ '/images/dummy-thumbnail.png', 'No screenshot' }
        % endif
    </li>
    % endfor
    <p>${ pager}</p>
    </ul>
% else:
    <p>No packages found.</p>
% endif
