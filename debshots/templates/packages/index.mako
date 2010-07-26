# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-index-header.mako"/>

<script type="application/x-javascript">
$(document).ready(function() {
    inithandlers();
});
</script>

## Include the contents of the first page of thumbnails/packages
<div id="ajaxarea">
<%include file="/packages/ajax-index.mako" />
</div>
