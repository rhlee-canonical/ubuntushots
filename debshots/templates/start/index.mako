# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<script type="application/x-javascript">
$(document).ready(function() {
    $('#rotated').cycle({
		fx: 'fade',
                timeout: 7000
	});
});
</script>

## Activate Lightbox plugin for screenshots DIV
<%include file="/packages/include-js-flyout.mako"/>

% if c.newest_screenshots:
<h1>Latest uploads</h1>
 <div id="rotated" style="width: 350px; height: 130px">
    % for pkg in c.packages_with_newest_screenshots:
        <% screenshot = pkg.screenshots[0] %>
        <div style="width: 345px; height: 125px">
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
        </div>
    % endfor
</div>
% endif
