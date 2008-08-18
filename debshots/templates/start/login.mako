# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

## Show login/logout form depending on whether a user is logged in
<div class="textbox">
% if not c.maintainer_id:
    <h1>Please login</h1>

    <p>
        Login here if you already have an account.
    </p>

    ${ h.tags.form('/start/loginsubmit', method='post') }
    <table>
    <tr>
        <td>Email address:</td>
        <td>${ h.tags.text('email', size=20) }</td>
    </tr>
    <tr>
        <td>Password:</td>
        <td>${ h.tags.password('password', size=20) }</td>
    </tr>
    </table>
    ${ h.tags.submit('login','Login') }
    % if c.error:
    <b>${c.error}</b>
    % endif
    </form>
% else:
    <h1>Logout</h1>

    <p>
        You are currently logged in as <i>${c.maintainer.email}</i>
    </p>

    ${ h.tags.form('/start/logout') }
    ${ h.tags.submit('logout','Logout') }
    </form>
% endif
</div>

<div class="textbox">
    <h1>Register (new users)</h1>

    <p>
        To be able to upload screenshots you will have to do
        a quick registration. Please tell us your email address
        username and we will send you a confirmation email.
    </p>

    ${ h.tags.form('/start/registersubmit', method='post') }
    <table>
    <tr>
        <td>Email address:</td>
        <td>${ h.tags.text('email', size=20) }</td>
    </tr>
    <tr>
        <td>Password:</td>
        <td>${ h.tags.password('password', size=20) }</td>
    </tr>
    </table>
    ${ h.tags.submit('login','Login') }
    </form>
</div>
