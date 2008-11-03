# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<script type="application/x-javascript">
    $(document).ready(function() {
        $('#username').focus();
    });
</script>


## Show login form for admins
<div class="graybox">
    <h1>Login</h1>
</div>

${ h.tags.form('/start/loginsubmit', method='post') }
<table>
<tr>
    <td>Username:</td>
    <td>${ h.tags.text('username', size=20, id='username') }</td>
</tr>
<tr>
    <td>Password:</td>
    <td>${ h.tags.password('password', size=20) }</td>
</tr>
</table>

% if c.error:
<b>${c.error}</b>
% endif

<p>
${ h.tags.submit('login','Login') }
</p>
</form>
