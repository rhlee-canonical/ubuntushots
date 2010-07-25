# -*- coding: utf-8 -*-
<!-- List of packages from ajax-index.mako -->
% if c.packages:
    <% pager = c.packages.pager('Page: $link_previous $link_next ~10~') %>
    <ul class="quicksand">
    <p>${ pager}</p>
    % for package in c.packages:
    <li data-id="pkg-${ package.id }" style="position: relative">
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
        % else:
            ## Show dummy screenshot
            ${ h.tags.image('/images/dummy-thumbnail.png', 'No screenshot') }
        % endif
        <div class="textcenter" style="bottom: 5px; position: absolute; width: 160px">
            ${ h.tags.link_to(package.name, h.url('package', package=package.name)) }
        </div>
    </li>
    % endfor
    <p>${ pager}</p>
    </ul>
% else:
    <p>No packages found.</p>
% endif
