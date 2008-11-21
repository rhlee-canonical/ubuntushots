# -*- coding: utf-8 -*-
import logging
from debshots.lib.base import *
import os
import PIL.Image
import StringIO
import paste
from debshots.lib import my, validators
import formencode

log = logging.getLogger(__name__)

class ValidateExistingDebianPackage(formencode.Schema):
    """formencode validation schema for uploading new screenshots"""
    packagename = validators.ValidatorDebianPackage(not_empty=True)
    version = formencode.validators.String(max=50)
    file = formencode.validators.FieldStorageUploadConverter(not_empty=True)
    allow_extra_fields = True

class PackagesController(BaseController):
    def index(self):
        """Show a list of packages with screenshots"""
        packages = model.Package.q()

        # Search for word
        search = request.params.get('search')
        if search:
            packages = packages.filter(
                (model.Package.name.like('%'+search+'%'))
                |
                (model.Package.description.ilike('%'+search+'%'))
            )

        # Search for debtag
        debtags_search = request.params.get('debtag')
        if debtags_search:
            db_debtag = model.Debtag.q().filter_by(tag=unicode(debtags_search)).first()
            if not db_debtag:
                abort(404, 'Sorry, no packages with this debtag could be found.')
            packages = packages.join('debtags').filter(model.Debtag.tag==unicode(debtags_search))

        # Only show packages with approved screenshots or the user's own screenshots
        # (JOINing reduces the packages to those which have corresponding screenshots)
        packages = packages.join('screenshots')
        packages = packages.filter(
            (model.Screenshot.approved==True)
            |
            (model.Screenshot.uploaderhash==my.client_cookie_hash())
            )
        packages = packages.options(model.orm.eagerload('screenshots'))

        c.packages = h.paginate.Page(packages,
            items_per_page=20,
            page=request.params.get('page',0),
            search=search,
            debtag=debtags_search,
            )

        return render('/packages/index.mako')

    def without_screenshots(self):
        """Show a list of packages without screenshots"""
        packages = model.packages_without_screenshots()

        packages = packages.options(model.orm.eagerload('screenshots'))

        # Filter for search word if provided
        search = request.params.get('search')
        if search:
            packages = packages.filter(
                (model.Package.name.like('%'+search+'%'))
                |
                (model.Package.description.ilike('%'+search+'%'))
            )

        c.packages = h.paginate.Page(packages,
            items_per_page=10,
            page=request.params.get('page',0),
            search=search)
        return render('/packages/index.mako')

    def moderate(self):
        """Show a list of not-yet-approved screenshots for the admin"""
        # Admins only
        if 'username' not in session:
            abort(403)
        packages = model.packages_with_moderated_screenshots()
        c.packages = h.paginate.Page(
            packages,
            page=request.params.get('page',0),
            items_per_page=1,
            )
        return render('/packages/moderate-index.mako')

    def upload(self, package):
        """Show package upload dialog"""
        c.packagename=package
        return render('/packages/upload.mako')

    def uploadfile(self):
        """Deal with uploaded screenshot"""
        # Validate the upload form
        try:
            fields = my.validate(ValidateExistingDebianPackage)
        except formencode.Invalid, e:
            return my.htmlfill(self.upload(None), e)
        package = fields['packagename']
        filename = fields['file']
        error = _process_screenshot(
            filehandle=filename.file,
            package=package.name,
            version=fields['version'])
        if error:
            c.message=error
            my.message(error)
        else:
            log.info("Screenshot uploaded for package '%s'", package.name)
            my.message("Screenshot for package '%s' uploaded successfully."
                % package.name)

        return render('/packages/upload.mako')

    def show(self, package):
        """Show a page with details and screenshots of a package"""
        c.package = model.Package.q().filter_by(name=package).first()
        if not c.package:
            abort(404)
            # TODO: display a page that proposed to upload screenshots as none yet exist

        c.title = 'Package ' + c.package.name

        return render('/packages/show.mako')

    def _image(self, id, size):
        """Return an image or None if there is no such image."""
        if not id:
            return None

        screenshot = model.Screenshot.q().get(id)

        # Make sure the screenshot database row is available
        if not screenshot:
            return None

        # only show images that are approved (or for admins or owners)
        if not my.authorized_for_screenshot(screenshot):
            return None

        file_path = os.path.join(screenshot.directory, '%s_%s.png' % (id, size))

        # Make sure the file on disk exists
        if not os.path.isfile(file_path):
            # The file is in the database but not on disk? Remove it from the database then.
            log.error("Screenshot file #%s missing on disk. Removing screenshot from database." % screenshot.id)
            db.delete(screenshot)
            db.commit()
            return None

        return self._image_fileapp(file_path)

    def _image_fileapp(self, file_path):
        """Return a static image from a path via a FileApp"""
        fapp = paste.fileapp.FileApp(
            file_path,
            headers=[
                ('Content-Type', 'image/png'),
                # make images cacheable
                ('Cache-Control', 'public, max-age=86400'),
                ('Pragma', ''),
            ])
        return fapp(request.environ, self.start_response)

    def image(self, id, size):
        """Return the binary PNG image for <img src...> tags

        id: id number of the image in the database"""
        # Try to retrieve a WSGI fileapp for this image
        image_fapp = self._image(id, size)

        if not image_fapp:
            abort(404)

        return image_fapp

    def static_image(self, package_inital, package, id, size):
        """Return the binary PNG image for an approved screenshots (without database calls)

        This is a fast method to serve screenshots without calling for information
        from the database. Actually static images should directly get served from
        the web server. But if /screenshots/... is handled through Pylons then this
        method is used as a fallback."""
        file_path = os.path.join(
            config['debshots.screenshots_directory'],
            'approved',
            package_inital,
            package,
            '%s_%s.png' % (id, size))
        log.debug("Serving static image from %s", file_path)
        if not os.path.isfile(file_path):
            log.warn("Image file %s not found" % file_path)
            abort(404)

        return self._image_fileapp(file_path)

    def thumbnail(self, package):
        """Return a thumbnail image or a dummy image for a certain package."""
        if not package:
            return self._dummy_thumbnail()

        this_package = model.Package.q().filter_by(name=package).first()

        # Given package is not in the database
        if not this_package:
            return self._dummy_thumbnail()

        # Package does not have screenshots yet
        if not this_package.screenshots:
            return self._dummy_thumbnail()

        first_screenshot = this_package.screenshots[0]
        return self._image_fileapp(first_screenshot.image_path('small'))

    def screenshot(self, package):
        """Return a large image or a dummy image for a certain package."""
        if not package:
            return self._dummy_screenshot()

        this_package = model.Package.q().filter_by(name=package).first()

        # Given package is not in the database
        if not this_package:
            return self._dummy_screenshot()

        # Package does not have screenshots yet
        if not this_package.screenshots:
            return self._dummy_screenshot()

        first_screenshot = this_package.screenshots[0]
        return self._image_fileapp(first_screenshot.image_path('large'))

    def _dummy_thumbnail(self):
        """Return 160x120 dummy thumbnail"""
        image_path = os.path.join(
            config['pylons.paths']['static_files'],
            'images/dummy-thumbnail.png'
            )
        fapp = paste.fileapp.FileApp(image_path,
            headers=[('Content-Type', 'image/png')])
        return fapp(request.environ, self.start_response)

    def _dummy_screenshot(self):
        """Return 800x600 dummy screenshot"""
        image_path = os.path.join(
            config['pylons.paths']['static_files'],
            'images/dummy-screenshot.png'
            )
        fapp = paste.fileapp.FileApp(image_path,
            headers=[('Content-Type', 'image/png')])
        return fapp(request.environ, self.start_response)

    def delete_screenshot(self, screenshot):
        this_screenshot = model.Screenshot.q().get(screenshot)
        if not this_screenshot:
            abort(404)

        package = this_screenshot.package

        # Make sure the user is allowed to delete the screenshot!
        if not my.authorized_for_screenshot(this_screenshot):
            abort(403, "I'm afraid I can't do that, Dave.")

        # Admins or the one who uploaded the screenshot is allowed to delete
        elif ('username' in session) or (my.client_cookie_hash() == this_screenshot.uploaderhash):
            db.delete(this_screenshot)
            for image_path in this_screenshot.image_paths:
                if os.path.isfile(image_path):
                    os.unlink(image_path)
            my.message('Screenshot for package <em>%s</em> deleted.' % package.name)
        # If the screenshot is 'approved' and the current user is not an admin
        # then it's only possible to mark the screenshot for deletion by an admin.
        else:
            this_screenshot.markedfordelete=True
            this_screenshot.delete_reason=request.params.get('reason','?')[:100]
            my.message('Admins will be asked to delete this screenshot.')

        db.commit()

        # The approved screenshots have changes. Remove the cached start page.
        g.cache.delete('debshots:front_page') # could make it add the new render explicitly later

        # Try to redirect to the backlink (if provided)
        my.redirect_back()

        # Otherwise redirect to the package overview
        redirect_to(h.url_for('package', package=package.name))

    def approve_screenshot(self, screenshot):
        """Approve a screenshot. Sets it to status 'approved'."""
        this_screenshot = model.Screenshot.q().get(screenshot)
        if not this_screenshot:
            abort(404)

        if this_screenshot.approved:
            my.message("Screenshot for package <em>%s</em> already approved." % package.name)
            my.redirect_back()
            redirect_to(h.url_for('package', package=package.name))

        package = this_screenshot.package

        # Make sure the user is allowed to delete the screenshot!
        # Has this screenshot been uploaded by the current user?
        if not my.authorized_for_screenshot(this_screenshot):
            abort(403, "I'm afraid I can't do that, Dave.")

        old_image_paths = this_screenshot.image_paths
        this_screenshot.approved = True
        new_image_paths = this_screenshot.image_paths

        # sanity check
        assert(len(old_image_paths) == len(new_image_paths))

        try:
            for old_path, new_path in zip(old_image_paths, new_image_paths):
                if not os.path.isdir(this_screenshot.directory):
                    log.debug("Creating new directory %s", this_screenshot.directory)
                    os.makedirs(this_screenshot.directory)
                log.debug("Renaming %s to %s", old_path, new_path)
                os.rename(old_path, new_path)
            db.commit()
        except IOError:
            raise

        my.message("Screenshot for package <em>%s</em> approved." % package.name)

        # The approved screenshots have changes. Remove the cached start page.
        g.cache.delete('debshots:front_page') # could make it add the new render explicitly later

        my.redirect_back()
        redirect_to(h.url_for('package', package=package.name))

    def keep_screenshot(self, screenshot):
        """Remove a screenshot's "markedfordelete" tag.

        This action is called if an admin decides to keep a certain screenshot although
        a visitor requested that this screenshot gets deleted."""
        this_screenshot = model.Screenshot.q().get(screenshot)
        if not this_screenshot:
            abort(404)

        package = this_screenshot.package

        # Admins only
        if not 'username' in session:
            abort(403, "I'm afraid I can't do that, Dave.")
        this_screenshot.markedfordelete=False
        db.commit()

        my.message("Screenshot for package <em>%s</em> kept." % package.name)

        my.redirect_back()
        redirect_to(h.url_for('moderate', package=package.name))

    def ajax_autocomplete_packages(self):
        """Get a list of packages for the autocompleter"""
        query = request.params.get('q')
        packages = model.Package.q().filter(model.Package.name.startswith(query))[:30]
        return '\n'.join(["%s|%s" % (package.name, package.description) for package in packages])

    @jsonify
    def ajax_get_version_for_package(self):
        """Get the current version of a package from the database"""
        query = request.params.get('q')
        package = model.Package.q().filter_by(name=query).first()
        if not package:
            return ''
        logging.debug('ajax_get_version_for_package(%s) -> %s' % (query, package.version))
        return { 'version' : package.version }

#--------------------------


def _process_screenshot(filehandle, package, version):
    """Process the uploaded PNG file

    - resize to no larger than 800x600
    - resize (thumbnail) to no larger than 160x120
    - insert into database as Screenshot
    """
    try:
        image = PIL.Image.open(filehandle)
    except IOError, e:
        return "The file you uploaded is not a valid PNG image"

    log.debug(u"Image dimensions: %s x %s" % image.size)
    log.debug(u"Image format: %s" % image.format)

    if image.format != 'PNG':
        return "Your image file was not in PNG format"

    # Is there a database entry for this package already?
    log.debug("Fetch package entry from database for package '%s'", package)
    db_pkg = model.Package.q().filter_by(name=package).first()
    if not db_pkg: # otherwise create one
        log.debug("No package entry found. Creating a new one.")
        db_pkg = model.Package(name=package)
        db.save(db_pkg)

    image_types = model.image_types
    to_save = []
    try:
        for image_type in image_types:
            image_copy = image.copy()
            image_copy.thumbnail(image_type['size'], PIL.Image.ANTIALIAS)
            #imgc.convert('RGB')
            to_save.append((image_copy, image_type))
    except IOError, e:
        return "There seems to be a problem with your image: %s" % e

    # Create screenshot entry
    db_screenshot = model.Screenshot(
        uploaderip=my.client_ip(),
        uploaderhash=my.client_cookie_hash(),
        version=version,
    )
    # Screenshots uploaded by admins are automatically approved
    if 'username' in session:
        db_screenshot.approved = True

    db_pkg.screenshots.append(db_screenshot)

    db.commit()

    # Create the package's screenshots path if it does not exist yet
    if not os.path.isdir(db_screenshot.directory):
        log.debug("Create destination directory: %s", db_screenshot.directory)
        os.makedirs(db_screenshot.directory)

    for image, image_type in to_save:
        image_path = os.path.join(db_screenshot.directory, '%s_%s.png' % (db_screenshot.id, image_type['extension']))
        log.debug("Saving %s image to %s" % (image_type['size'], image_path))
        image.save(image_path)

    return None # Success
