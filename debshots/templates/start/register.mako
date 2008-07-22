# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<h1>New user registration</h1>

${ h.tags.form('/start/registersubmit', method='post') }
<p>
    To be able to upload screenshots you will have to do
    a quick registration. Please tell us your Debian
    username and we will send you a confirmation email to your
    Debian email address.
</p>

${ h.tags.text('debianuser', size=20) }@debian.org
<br />
${ h.tags.submit('register','Register') }
</form>
