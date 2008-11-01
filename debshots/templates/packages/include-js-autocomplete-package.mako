<script type="application/x-javascript">
    $(document).ready(function() {
        $('#packagename').autocomplete(
            '/packages/ajax_autocomplete_packages',
            {
            minChars: 2,
            mustMatch: true,
            formatItem: formatPackage,
            max: 30,
            delay: 200
            }
        );

        ## Focus on first input field
        $('#packagename').focus();
    });

    ## Formatting function for autocomplete results (shows description)
    function formatPackage(row) {
        return row[0] + '<br /><span class="ac_descr">' + row[1] + '</span>';
    };
</script>
