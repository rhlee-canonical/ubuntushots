# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-index-header.mako"/>
<%include file="/packages/include-js-flyout.mako"/>

<script type="application/x-javascript">
$(document).ready(function() {
    $('#screenshots').cycle({
		fx: 'fade',
                timeout: 3000
	});
});
</script>

<div id="ajaxarea">
<h1>AJAX AREA!</h1>

<%include file="/packages/ajax-index.mako" />

<!--<p style="clear: both"></p>-->

</div>
