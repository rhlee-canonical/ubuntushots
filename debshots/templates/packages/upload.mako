# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-js-autocomplete-package.mako"/>

<h1>Upload screenshots</h1>

<p>Please enter the name of the package you wish to upload a screenshot for:</p>

${ h.tags.form(h.url_for('uploadfile'), method='post', multipart=True) }
<table>
<tr>
    <td>Package:</td>
    <td>
        <input type="text" name="packagename" id="packagename" size="40" /> (just type the first letters)
    </td>
</tr>
<tr>
    <td>Screenshot:</td>
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
