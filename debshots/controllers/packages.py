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
        search = request.params.get('search')
        # TODO: only print packages with 0 unapproved screenshots
        if search:
            packages = packages.filter(
                (model.Package.name.like('%'+search+'%'))
                |
                (model.Package.description.ilike('%'+search+'%'))
            )
        # Only show packages with approved screenshots or the user's own screenshots
        # (JOINing reduces the packages to those which have corresponding screenshots)
        packages = packages.join('screenshots')
        packages = packages.filter(
            (model.Screenshot.approved==True)
            |
            (model.Screenshot.uploaderhash==my.client_cookie_hash())
            )

        c.packages = h.paginate.Page(packages,
            items_per_page=10,
            page=request.params.get('page',0),
            search=search,
            )
        return render('/packages/index.mako')

    def without_screenshots(self):
        """Show a lit of packages without screenshots"""
        packages = model.Package.q()
        # Only show packages with screenshots
        packages = packages.filter(~model.Package.screenshots.any())

        # TODO: the subselect run by .any() is pretty slow. can we optimize that?

        c.packages = h.paginate.Page(packages,
            items_per_page=10,
            page=request.params.get('page',0))
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
            return my.htmlfill(self.upload(), e)
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
            log.info("Screenshot uploaded for package '%s'" % package.name)
            my.message("Screenshot for package '%s' uploaded successfully."
                % package.name)

        return render('/packages/upload.mako')

    def show(self, package):
        """Show a page with details and screenshots of a package"""
        c.package = model.Package.q().filter_by(name=package).first()
        if not c.package:
            abort(404)
            # TODO: display a page that proposed to upload screenshots as none yet exist
        return render('/packages/show.mako')

    def image(self, id):
        """Return the binary PNG image for <img src...> tags

        id: id number of the image in the database"""
        # Try to retrieve a WSGI fileapp for this image
        image_fapp = self._image(id)

        if not image_fapp:
            abort(404)

        return image_fapp

    def thumbnail(self, package):
        """Return a thumbnail image or a dummy image for a certain package."""
        if not package:
            return self._dummy_thumbnail()

        this_package = model.Package.q().filter_by(name=package).first()

        # Given package is not in the database
        if not this_package:
            return self._dummy_thumbnail()

        # Package does not have screenshots yet
        if this_package.screenshots.count() == 0:
            return self._dummy_thumbnail()

        first_screenshot = this_package.screenshots[0]
        return self.image(first_screenshot.small_image.id)

    def _image(self, id):
        """Return an image or None if there is no such image."""
        if not id:
            return None

        image = model.Image.q().get(id)

        # Make sure the screenshot database row is available
        if not image:
            return None

        # only show images that are approved (or for admins or owners)
        if not my.authorized_for_screenshot(image.screenshot):
            return None

        # Make sure the file on disk exists
        if not os.path.isfile(image.path):
            # The file is in the database but not on disk? Remove it from the database then.
            log.error("Image file #%s missing on disk. Removing screenshot from database." % image.id)
            db.delete(image.screenshot)
            db.commit()
            return None
        fapp = paste.fileapp.FileApp(image.path,
            headers=[
                ('Content-Type', 'image/png'),
                ('Cache-Control', 'max-age=86400')
            ])
        return fapp(request.environ, self.start_response)

    def _dummy_thumbnail(self):
        """Return 160x120 dummy thumbnail"""
        image_path = os.path.join(
            config['pylons.paths']['static_files'],
            'images/dummy-thumbnail.png'
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
            for image in this_screenshot.images:
                if os.path.isfile(image.path):
                    os.unlink(image.path)
            my.message('Screenshot for package <em>%s</em> deleted.' % package.name)
        # If the screenshot is 'approved' and the current user is not an admin
        # then it's only possible to mark the screenshot for deletion by an admin.
        else:
            this_screenshot.markedfordelete=True
            this_screenshot.delete_reason=request.params.get('reason','?')
            my.message('Admins will be asked to delete this screenshot.')

        db.commit()

        # Try to redirect to the backlink (if provided)
        my.redirect_back()

        # Otherwise redirect to the package overview
        redirect_to(h.url_for('package', package=package.name))

    def approve_screenshot(self, screenshot):
        """Approve a screenshot. Sets it to status 'approved'."""
        this_screenshot = model.Screenshot.q().get(screenshot)
        if not this_screenshot:
            abort(404)

        package = this_screenshot.package

        # Make sure the user is allowed to delete the screenshot!
        # Has this screenshot been uploaded by the current user?
        if not my.authorized_for_screenshot(this_screenshot):
            abort(403, "I'm afraid I can't do that, Dave.")
        this_screenshot.approved=True
        db.commit()

        my.message("Screenshot for package <em>%s</em> approved." % package.name)

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
    - insert into database as Screenshot and two Image objects
    """
    image = filehandle.read()
    stringio_image = StringIO.StringIO(image)
    # Load file into PIL (Python Imaging Libary) Image object
    try:
        pil = PIL.Image.open(stringio_image)
    except IOError, e:
        return "The file you uploaded is not a valid PNG image"

    log.debug(u"Image dimensions: %s x %s" % pil.size)
    log.debug(u"Image format: %s" % pil.format)

    if pil.format != 'PNG':
        return "Your image file was not in PNG format"

    # Is there a database entry for this package already?
    log.debug("Fetch package entry from database for package '%s'" % package)
    db_pkg = model.Package.q().filter_by(name=package).first()
    if not db_pkg: # otherwise create one
        log.debug("No package entry found. Creating a new one.")
        db_pkg = model.Package(name=package)
        db.save(db_pkg)

    # Resize to 800x600
    try:
        image_800_600, xsize, ysize = _resize(pil, 800, 600)
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
        db_screenshot.approved=True

    db_pkg.screenshots.append(db_screenshot)

    # Create large image entry
    db_image_large = model.Image(
        xsize=xsize,
        ysize=ysize,
        large=True,
        )

    # Resize to 160x120
    image_160_120, xsize, ysize = _resize(pil, 160, 120)

    # Create small image entry
    db_image_small = model.Image(
        xsize=xsize,
        ysize=ysize,
        large=False,
        )

    db_screenshot.images.append(db_image_large)
    db_screenshot.images.append(db_image_small)
    db.commit()

    # Create the package's screenshots path if it does not exist yet
    # (As small images are saved into the same directory we just use db_image_large here)
    if not os.path.isdir(db_screenshot.directory):
        log.debug("Create destination directory: %s" % db_screenshot.directory)
        os.makedirs(db_screenshot.directory)
    log.debug("Saving large image to %s" % db_image_large.path)
    image_800_600.save(db_image_large.path, format='PNG')

    log.debug("Saving small image to %s" % db_image_large.path)
    image_160_120.save(db_image_small.path, format='PNG')

    return None # Success

def _resize(image, xmax, ymax):
    """Resize image to a maximal given size while retaining its aspect"""
    log.debug("Resizing image to %sx%s" % (xmax,ymax))
    xold, yold = image.size
    xold = float(xold)
    yold = float(yold)
    xmax = float(xmax)
    ymax = float(ymax)
    xnew = None
    ynew = None

    # Image has the right size or is smaller than x/y?
    if xold<=xmax and yold<=ymax:
        log.debug("Image is already smaller than %ix%i - no conversion necessary" % (xmax,ymax))
        xnew = xold
        ynew = yold
    # Image too large
    else:
        # Image too wide for a x/y ratio?
        if xold/yold > xmax/ymax:
            xnew = xmax
            ynew = yold*xmax/xold
            log.debug("Image too wide for %ix%i. Resizing to %ix%i" % (xmax,ymax,xnew,ynew))
        # Image too high for a x/y ratio?
        else:
            xnew = xold*ymax/yold
            ynew = ymax
            log.debug("Image too high for %ix%i. Resizing to %ix%i" % (xmax,ymax,xnew,ynew))

        log.debug("Image will be resized to: %i x %i" % (xnew, ynew))
        image = image.resize((int(xnew), int(ynew)), PIL.Image.ANTIALIAS)

    return image, xnew, ynew
