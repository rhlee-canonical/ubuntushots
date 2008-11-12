# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-js-autocomplete-package.mako"/>

<script type="application/x-javascript">
    $(document).ready(function() {
        $('#autocompletehint').html('(just type the first letters)');

        $('#packagename').change(
            function () {
                // Get the current package version from the database
                package = $('#packagename').val();

                $.getJSON(
                    '/packages/ajax_get_version_for_package',
                    { q: package },
                    function (data) {
                        $('#version').val(data.version);
                        }
                    )
                }
            );
    });
</script>


<h1>Upload screenshots</h1>

<p>Please enter the name of the package you wish to upload a screenshot for:</p>

${ h.tags.form(h.url_for('uploadfile'), method='post', multipart=True) }
<table>
<tr>
    <td>Package name:</td>
    <td>
        <input type="text" name="packagename" id="packagename" size="40" />
        <span id="autocompletehint"></span>
    </td>
</tr>
<tr>
    <td>Software version:</td>
    <td>
        <input type="text" name="version" id="version" size="40" /> (optional)
    </td>
</tr>
<tr>
    <td>Screenshot (PNG file):</td>
    <td>
        <input type="file" name="file" size="40"/>
    </td>
</tr>
</table>
<input type="submit" value="Upload screenshot" />
</form>

% if c.message:
<p><i>${ c.message }</i></p>
% endif
