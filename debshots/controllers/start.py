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

    debianuser = formencode.validators.Regex(r'^[a-z]+$')

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
            fields = my.validate(ValidateLogin)
        except formencode.Invalid, e:
            return my.htmlfill(self.login(), e)

        user = model.User.q().filter_by(
            name=fields['username'],
            passwordhash=md5.new(fields['password']).hexdigest()).first()

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

        # TODO: check if user account is already verified/activated

        sender_address = config['debshots.email_sender']
        #recipient_address = fields['debianuser']+'@debian.org'
        # TODO: testing address currently...
        recipient_address='email@christoph-haas.de'

        # Create a new user account or get the existing account
        user = model.User.q().filter_by(name=fields['debianuser']).first()
        if not user: # create if not yet existing
            user = model.User()
            model.Session.save(user)

        # Set a randomly generated activation in the user account
        activation_code = md5.new(unicode(random.random())).hexdigest()
        user.name = fields['debianuser']
        user.hash = activation_code
        user.passwordhash = md5.new(fields['password']).hexdigest()
        model.Session.commit()

        c.debianuser = fields['debianuser']

        # Generate an email
        c.activation_link = h.url_for(
            'activate',
            hash=activation_code,
            user=fields['debianuser'],
            qualified=True)
        message = render('/email/verification.mako')

        log.debug('Sending verification email (hash=%s, user=%s)'
                % (activation_code, fields['debianuser']))

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

    def activate(self, user, hash):
        """Activate a user account.

        This action is called from an email that a new user gets
        sent to verify the email address."""
        log.debug("Trying to activate user account (user=%s, hash=%s)"
            % (user, hash))
        user = model.User.q().filter_by(name=user).first()
        if user.verified == True:
            # TODO: proper HTML response
            return "Your account has already been activated."
        if not user: # create if not yet existing
            # TODO: proper HTML response
            return "We cannot find your registration request. :("
        if user.hash != hash:
            # TODO: proper HTML response
            return "Your registration failed. Did you use the wrong link?"

        user.hash = ''
        user.verified = True
        model.Session.commit()
        # TODO: proper HTML response
        return "Your account was activated."
