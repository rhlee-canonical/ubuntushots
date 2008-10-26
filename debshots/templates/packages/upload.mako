# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<h1>Upload screenshots</h1>

<p>Please enter the name of the package you wish to upload a screenshot for:</p>

${ h.tags.form(h.url_for('uploadfile'), method='post') }
Package: <input type="text" name="packagename" size="20" />
<br />
Screenshot: <input type="file" name="file"/>
</form>
