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
    password = formencode.validators.String(max=50, not_empty=True)

class ValidateRegister(formencode.Schema):
    allow_extra_fields = True

    debianuser = formencode.validators.Regex(r'\w+')

class StartController(BaseController):

    def index(self):
        """Welcome page"""
        return render('/start/index.mako')

    def login(self):
        """Show login form"""
        return render('/start/login.mako')

    def loginsubmit(self):
        """Process login form"""
        # Validate input fields
        try:
            fields = my.validate(validators.ValidateLogin)
        except formencode.Invalid, e:
            return my.htmlfill(self.login(), e)

        user = model.User.q().filter_by(
            username=fields['username'],
            password=fields['password']).first()

        if not user:
            log.info("Login failed: %s" % fields['username'])
            return render("/start/login.mako", error='Login failed')

        log.info("User logged in: %s" % (fields['username']))

        # Set a cookie session variable to mark the user as logged in
        session['user']=user.id
        session.save()
        return render("/start/index.mako")

    def logout(self):
        """Logout user"""
        if 'user' in session:
            del session['user']
            session.save()
        return render("/start/index.mako")

    def register(self):
        """Show registration form"""
        return render("/start/register.mako")

    def registersubmit(self):
        """Process registration form and send verification email"""

        # Formular-Eingaben validieren
        try:
            fields = my.validate(ValidateRegister)
        except formencode.Invalid, e:
            return my.htmlfill(self.register(), e)

        sender_address = config['debshots.email_sender']
        recipient_address = fields['debianuser']+'@debian.org'

        # Create a new user account
        new_user = model.User()

        # Set a randomly generated activation in the user account
        activation_code = md5.new(str(random.random())).hexdigest()
        new_user.name = fields['debianuser']
        new_user.hash = activation_code
        model.Session.save(new_user)
        model.Session.commit()

        # Generate an email
        c.verification_email = h.url_for(
            controller='start',
            action='activate',
            id=activation_code,
            qualified=True
        )
        message = render('/email/verification.mako')

        # Send the email
        log.debug('Starting SMTP session to %s' % config['global_conf']['smtp_server'])
        smtp_session = smtplib.SMTP(config['global_conf']['smtp_server'])

        if 'smtp_username' in config['global_conf']:
            log.debug('Sending SMTP authentication')
            smtp_session.login(
                config['global_conf']['smtp_username'],
                config['global_conf']['smtp_password'])

        log.debug('Sending email to %s' % (recipient_address,))
        error = smtp_session.sendmail(sender_address, [recipient_address], message)

        if error:
            log.critical('Failed sending email to %s' % (recipient_address,))
        else:
            log.debug('Email sent to %s successfully' % (recipient_address,))

        return render("/start/registration_pending.mako")