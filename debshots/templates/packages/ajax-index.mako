# -*- coding: utf-8 -*-
<!-- List of packages from ajax-index.mako -->

% if c.packages:
    <script type="application/x-javascript">

        ## Define a function that gets called if the user clicks on a new page number.
        function pager_goto(url) {
            ## Dim the div.ajaxrea and load the new page
            $('#ajaxarea').css('opacity', 0.5).load(url);
        };

        $(document).ready(function() {
            ## Set div.ajaxarea back to full opaqueness
            $('#ajaxarea').css('opacity', 1);
            inithandlers();
        });
    </script>

    <%
        pager = c.packages.pager('Page: $link_previous ~10~ $link_next ',
            symbol_previous=h.tags.literal("&larr;"),
            symbol_next=h.tags.literal("&rarr;"),
            onclick="pager_goto('$partial_url'); return false")
    %>
    <p>${ pager}</p>
    <ul class="quicksand" id="quicksand">
    % for package in c.packages:
    <li data-id="pkg-${ package.id }" style="position: relative">
        ##<i>${ package.description }</i>
        ##${ package.section }
        ## Show link to upload screenshots
        ##${ h.tags.link_to('Upload a screenshot', h.url('upload', package=package.name)) }
        ## Second line shows screenshots
        <% my_or_approved_screenshots = package.my_or_approved_screenshots %>
        % if my_or_approved_screenshots:
            <div class="screenshots">
            % for screenshot in my_or_approved_screenshots:
                <a class="image" href="${screenshot.large_image_url}"
                    title="Screenshot of package '${screenshot.package.name}'">
                    <img src="${screenshot.small_image_url}" alt="Screenshot" />
                </a>
            % endfor
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
    </ul>
% else:
    <p>No packages found.</p>
% endif
