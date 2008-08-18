# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<div class="textbox">
    <h1>What is screenshots.debian.net?</h1>
    <p>
        Several developers proposed a service that provides screenshots for the
        applications provided as Debian packages. This is an effort by
        Christoph Haas to provide a web service that hosts screenshots.
        Maintainers of the respective packages are invited to upload
        screenshots for their application here.
    </p>

    <p>
        If all goes well this service can be integrated into other Debian services
        like <i>packages.debian.org</i> or even package managers like <i>synaptic</i>.
    </p>
</div>

<div class="textbox">
    <h1>Upload screenshots</h1>
    <p>
        You need to be registered so your email address can be verified.
        Please click on <i>Login/Register</i> on the top and sign up for an account.
        You will get a confirmation email sent to the address you give
        with a confirmation URL.
    </p>

    <p>
        Once you have a verified account you can upload your packages
        directly via the web interface. A command line tool to aid
        the administration of screenshots may come later.
    </p>

    <p>
        You don't need to be a Debian developer to upload screenshots.
        You can administer screenshots for all packages where you are
        listed in the <i>Maintainer</i> or <i>Uploader</i> field of the
        source control file.
    </p>
</div>

<div class="textbox">
    <h1>Accessing the screenshots</h1>
    <p>
        Click on <i>Screenshots</i> on the top or
        use these URL formats to get the screenshots:
    </p>

    <ul>
        <li>
            http://screenshots.debian.net/packages
            <br/>
            (List of all packages with screenshots)
        </li>
        <li>
            http://screenshots.debian.net/screenshots/foobar
            <br/>
            (List of screenshots for package 'foobar')
        </li>
        <li>
            http://screenshots.debian.net/screenshot/foobar
            <br/>
            (First screenshot for package 'foobar' to be used in img/src tags)
        </li>
</div>
