# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>


<script type="application/x-javascript">
$(document).ready(function() {
    inithandlers();

    $('input[name=search]').focus();
});
</script>


<div class="graybox">
    <h1>Browsing screenshots</h1>
    ${ h.tags.form(h.url.current())}
        <p>
            ${ h.tags.link_to('All packages',
                h.url('packages',
                    search=request.params.get('search',''),
                    debtag=request.params.get('debtag','')))}
            |
            ${ h.tags.link_to('Packages with screenshots only',
                h.url('packages-with-screenshots',
                    search=request.params.get('search',''),
                    debtag=request.params.get('debtag','')))}
            |
            ${ h.tags.link_to('Packages without screenshots only',
                h.url('packages-without-screenshots',
                    search=request.params.get('search',''),
                    debtag=request.params.get('debtag','')))}

            ## Admin options:
            % if 'username' in session:
            |
            <a href="/packages/moderate">Moderation queue</a>
            % endif
        </p>
        <p>
            ## Search field
            Search term: ${ h.tags.text(name='search', value=request.params.get('search')) }
            % if c.search_debtag_description:
            | With debtag: ${ c.search_debtag_description }
            % endif
        </p>
        <div>
            <input type="submit" value="Show" />
        </div>
    </form>
</div>


% if c.packages:
    <%
        pager = c.packages.pager('Page: $link_previous ~10~ $link_next ',
            symbol_previous=h.tags.literal("&larr;"),
            symbol_next=h.tags.literal("&rarr;"))
    %>
    <p>${ pager}</p>
    <table>
        <tr>
            % for nr,package in enumerate(c.packages):
                <td style="text-align: center; border: 4px solid #fff; min-width: 160px;">
                    ##<i>${ package.description }</i>
                    ##${ package.section }
                    ## Show link to upload screenshots
                    ##${ h.tags.link_to('Upload a screenshot', h.url('upload-pkg', package=package.name)) }
                    ## Second line shows screenshots
                    <% my_or_approved_screenshots = package.my_or_approved_screenshots %>
                    % if my_or_approved_screenshots:
                    <div class="screenshots cycle" style="height: 120px">
                        % for screenshot in my_or_approved_screenshots:
                            <a class="image" href="${screenshot.large_image_url}"
                                title="Screenshot of package '${screenshot.package.name}'">
                                <img src="${screenshot.small_image_url}" alt="Screenshot" />
                            </a>
                        % endfor
                    </div>
                    % else:
                    <div style="height: 120px">
                        ## Show dummy screenshot with link to upload
                        <a class="image" href="${h.url('upload-pkg',package=package.name)}">
                        ${ h.tags.image('/images/dummy-thumbnail-upload.png', 'No screenshot') }
                        </a>
                    </div>
                    % endif
                    </div>
                    <div class="imgcaption">
                        <a href="${h.url('package', package=package.name)}">
                        ${ package.name }
                        <br />
                        (<span class="smaller">${ package.description }</span>)
                        </a>
                    </div>
                    </td>
                ## Five thumbnails per row - after that start a new table row
                % if nr % 5 == 4:
                    </tr><tr>
                % endif
            % endfor
        </tr>
    </table>
% else:
    <p>No packages found.</p>
% endif
