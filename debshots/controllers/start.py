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

    email = formencode.validators.String(max=100, not_empty=True)
    password = formencode.validators.String(max=50, not_empty=True)

class ValidateRegister(formencode.Schema):
    allow_extra_fields = True

    email = formencode.validators.Email()
    password = formencode.validators.String(min=6, max=50)

class StartController(BaseController):

    def index(self):
        """Welcome page"""
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

        maintainer = model.Maintainer.q().filter_by(
            email=fields['email'],
            password=md5.new(fields['password']+config['debshots.md5salt']).hexdigest()).first()

        if not maintainer:
            log.info("Login failed: %s" % fields['email'])
            c.error="Login failed"
            return render("/start/login.mako")

        log.info("Maintainer logged in: %s" % (fields['email']))

        # Set a cookie session variable to mark the maintainer as logged in
        session['maintainer']=maintainer.id
        session.save()
        redirect_to('/login')

    def logout(self):
        """Logout maintainer"""
        if 'maintainer' in session:
            del session['maintainer']
            session.save()
        redirect_to('/login')

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

        # TODO: check if maintainer account is already verified/activated

        sender_address = config['debshots.email_sender']
        recipient_address=fields['email']

        # Create a new maintainer account or get the existing account
        maintainer = model.Maintainer.q().filter_by(
            email=fields['email'], verified=True).first()
        if not maintainer: # create if not yet existing
            maintainer = model.Maintainer()
            model.Session.save(maintainer)

        # Set a randomly generated activation in the maintainer account
        activation_code = md5.new(unicode(random.random())).hexdigest()
        maintainer.email = fields['email']
        maintainer.hash = activation_code
        maintainer.password = md5.new(fields['password']+config['debshots.md5salt']).hexdigest()
        model.Session.commit()

        c.email = fields['email']

        # Generate an email
        c.activation_link = h.url_for(
            'activate',
            hash=activation_code,
            email=fields['email'],
            qualified=True)
        message = render('/email/verification.mako')

        log.debug('Sending verification email (hash=%s, email=%s)'
                % (activation_code, fields['email']))

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

    def activate(self, email, hash):
        """Activate a maintainer account.

        This action is called from an email that a new maintainer gets
        sent to verify the email address."""
        log.debug("Trying to activate maintainer account (email=%s, hash=%s)"
            % (email, hash))
        maintainer = model.Maintainer.q().filter_by(email=email).first()
        if not maintainer: # create if not yet existing
            c.title="Registration failed"
            c.message="We cannot find your registration request. :("
            return render('/message.mako')
        if maintainer.verified == True:
            c.title="Registration not necessary"
            c.message="Your account has already been activated."
            return render('/message.mako')
        if maintainer.hash != hash:
            c.title="Registration failed"
            c.message="Your registration failed. Did you use the wrong link?"
            return render('/message.mako')

        maintainer.hash = ''
        maintainer.verified = True
        model.Session.commit()

        # Log the user in
        session['maintainer']=maintainer.id
        session.save()

        c.title="Account activated"
        c.message="The registration process is done. Feel free to upload screenshots now."
        return render('/message.mako')
