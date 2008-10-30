# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<%include file="/packages/include-js-autocomplete-package.mako"/>

<h1>Upload screenshots</h1>

<p>Please enter the name of the package you wish to upload a screenshot for:</p>

${ h.tags.form(h.url_for('uploadfile'), method='post', multipart=True) }
Package: <input type="text" name="packagename" id="packagename" size="40" /> (just type the first letters)
<br />
Screenshot: <input type="file" name="file" size="40"/>
<br />
<input type="submit" value="Upload screenshot" />
</form>

% if c.message:
<p><i>${ c.message }</i></p>
% endif
