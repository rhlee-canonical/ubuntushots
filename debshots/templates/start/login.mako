# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<h1>Please login</h1>

${ h.tags.form('/start/loginsubmit', method='post') }
<table>
<tr>
    <td>Debian username:</td>
    <td>${ h.tags.text('username', size=20) }</td>
</tr>
<tr>
    <td>Password:</td>
    <td>${ h.tags.password('password', size=20) }</td>
</tr>
</table>
${ h.tags.submit('login','Login') }
