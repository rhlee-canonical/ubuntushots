# -*- coding: utf-8 -*-
import logging
import formencode
import smtplib
import random
import md5

from debshots.lib.base import *

log = logging.getLogger(__name__)

class ValidateLogin(formencode.Schema):
    allow_extra_fields = True

    username = formencode.validators.String(max=20, not_empty=True)
    password = formencode.validators.String(max=20, not_empty=True)

class ValidateRegister(formencode.Schema):
    allow_extra_fields = True

    username = my. formencode.validators.Email()
    password = formencode.validators.String(min=6, max=50)

class StartController(BaseController):

    def index(self):
        """Welcome page"""

        # Show newest screenshot if available
        newest_screenshots = model.newest_screenshots()
        if newest_screenshots.count():
            # Return up to 8 screenshots
            c.newest_screenshots = newest_screenshots[:8]

        return render('/start/index.mako')

    def guidelines(self):
        """Show the screenshot guidelines"""
        return render('/start/guidelines.mako')

    def login(self):
        """Show login form"""
        return render('/start/login.mako')

    def loginsubmit(self):
        """Process login form"""
        # Validate input fields
        try:
            fields = my.validate(ValidateLogin)
        except formencode.Invalid, e:
            return my.htmlfill(self.login(), e)

        admin = model.Admin.q().filter_by(
            username=fields['username'],
            passwordhash=md5.new(
                fields['password']+config['debshots.md5salt']).hexdigest()).first()

        if not admin:
            log.info("Login failed: %s", fields['username'])
            c.error="Login failed"
            return render('/start/login.mako')

        log.info("Admin logged in: %s", fields['username'])

        # Set a cookie session variable to mark the maintainer as logged in
        session['username'] = admin.username
        session.save()
        redirect_to('moderate')

    def logout(self):
        """Logout an admin"""
        if 'username' in session:
            del session['username']
            session.save()
        redirect_to('/')
