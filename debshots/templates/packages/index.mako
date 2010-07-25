# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-index-header.mako"/>
<script type="application/x-javascript" src="/javascript/handlers.js"></script>

<script type="application/x-javascript">
$(document).ready(function() {
    inithandlers();
});
</script>

<div id="ajaxarea">
<h1>AJAX AREA!</h1>

<%include file="/packages/ajax-index.mako" />

</div>
