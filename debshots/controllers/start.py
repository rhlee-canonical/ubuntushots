# -*- coding: utf-8 -*-
import logging
import formencode
import smtplib
import random
from hashlib import md5
import pygooglechart

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

        cached =  app_globals.cache.get('debshots:front_page')
        if cached is not None:
            return cached

        # Show newest screenshot if available
        newest_screenshots = model.newest_screenshots()
        if newest_screenshots.count():
            # Return up to 8 screenshots
            c.newest_screenshots = newest_screenshots[:8]

        # Show packages with newest screenshots
        c.packages_with_newest_screenshots = model.packages_with_newest_screenshots()[:10]

        # Count number of screenshots
        c.number_of_screenshots = db.query(model.Screenshot).count()

        rendered = render('/start/index.mako')
        app_globals.cache.set('debshots:front_page', rendered)
        return rendered

    def guidelines(self):
        """Deprecated link for guidelines page redirects to upload page"""
        redirect('/upload')

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
            passwordhash=md5(
                fields['password']+config['debshots.md5salt']).hexdigest()).first()

        if not admin:
            log.info("Login failed: %s", fields['username'])
            c.error="Login failed"
            return render('/start/login.mako')

        log.info("Admin user '%s' logged in successfully", fields['username'])

        # Set a cookie session variable to mark the maintainer as logged in
        session['username'] = admin.username
        session.save()
        redirect(url('moderate'))

    def logout(self):
        """Logout an admin"""
        if 'username' in session:
            del session['username']
            session.save()
        redirect('/')

    def about(self):
        """Show a web page with statistical and conceptual information."""
        packages = db.query(model.Package)
        packages = packages.distinct().join('screenshots')
        packages = packages.filter(model.Screenshot.approved==True)
        c.packages_with_screenshots_count = packages.count()
        c.packages_count = db.query(model.Package).count()
        c.screenshots_percentage = float(c.packages_with_screenshots_count) / float(c.packages_count) * 100
        c.screenshots_count = db.query(model.Screenshot).count()
        c.average_screenshots_per_package = float(c.screenshots_count) / float(c.packages_with_screenshots_count)

        # Collect information how many screenshots have been uploaded each month
        # and create a URL to the Google Chart API displaying it.
        # (There are no automatic axis labels so the graph sucks and I probably need
        # something like GNUPLOT to get proper graphs.)
        month_labels = [] # e.g "11"
        year_labels = [] # e.g. "2010"
        month_uploads = []
        total_uploads = 0 # counting the uploads so that we get absolute values
        # Get a list of screenshots uploaded each month for the past 24 months
        query = db.query(
            model.sql.func.count().label('count'),
            model.sql.extract('year',model.Screenshot.uploaddatetime).label('year'),
            model.sql.extract('month',model.Screenshot.uploaddatetime).label('month')
            ).group_by('year','month').order_by('year','month').limit(24).all()
        for count, year, month in query:
            total_uploads += count
            month_uploads.append(total_uploads)
            month_labels.append(int(month))
            if month==1:
                year_labels.append(int(year))
            else:
                year_labels.append('')

        chart = pygooglechart.SimpleLineChart(600, 200)
        chart.add_data(month_uploads)
        chart.set_axis_labels(pygooglechart.Axis.BOTTOM, month_labels)
        chart.set_axis_labels(pygooglechart.Axis.BOTTOM, year_labels)
        chart.set_axis_labels(pygooglechart.Axis.LEFT, [min(month_uploads), max(month_uploads)])
        c.chart_url = chart.get_url()

        c.repositories = config['debshots.packages_update_urls'].split()

        return render('/start/about.mako')
