# -*- coding: utf-8 -*-
## Enable flyout plugin on screenshots

<script type="application/x-javascript">
    $(document).ready(function() {
        ## Flyout shows the large screenshots when clicking on the thumbnails
        $('.screenshots a.image').flyout({
            loadingSrc:'/images/spinner.gif',
            outSpeed: 300,
            inSpeed: 300
        });
    });
</script>
