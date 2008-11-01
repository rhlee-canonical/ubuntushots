# -*- coding: utf-8 -*-
import logging
from debshots.lib.base import *
import os
import PIL.Image
import StringIO
import paste
from debshots.lib import my
import formencode

log = logging.getLogger(__name__)

class ValidateExistingDebianPackage(formencode.Schema):
    """formencode validation schema for uploading new screenshots"""
    packagename = my.ValidatorDebianPackage(not_empty=True)
    file = formencode.validators.FieldStorageUploadConverter(not_empty=True)
    allow_extra_fields = True

class PackagesController(BaseController):

    def index(self):
        """Show a list of packages with screenshots"""
        packages = model.Package.q()
        c.packages = h.paginate.Page(packages,
            page=int(request.params.get('page_nr', 0)))
        return render('/packages/index.mako')

    def upload(self):
        """Show package upload dialog"""
        return render('/packages/upload.mako')

    def uploadfile(self):
        """Deal with uploaded screenshot"""
        # Validate the upload form
        try:
            fields = my.validate(ValidateExistingDebianPackage)
        except formencode.Invalid, e:
            return my.htmlfill(self.upload(), e)
        cachepackage = fields['packagename']
        filename = fields['file']
        error = _process_screenshot(filehandle=filename.file, package=cachepackage.name)
        if error:
            c.message=error
        else:
            log.info("Screenshot uploaded for package '%s'" % cachepackage.name)
            c.message="Screenshot for package '%s' uploaded successfully." % cachepackage.name

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
        screenshot = model.Screenshot.q().get(id)
        # Make sure the screenshot database row is available
        if not screenshot:
            abort(404)
        # Make sure the file on disk exists
        if not os.path.isfile(screenshot.path):
            # The file is in the database but not on disk? Remove it from the database then.
            log.error("Screenshot file #%s missing on disk. Removing from database." % screenshot.id)
            db.delete(screenshot)
            db.commit()
            abort(404)
        fapp = paste.fileapp.FileApp(screenshot.path,
            headers=[('Content-Type', 'image/png')])
        return fapp(request.environ, self.start_response)

    def ajax_autocomplete_packages(self):
        """Get a list of packages for the autocompleter"""
        query = request.params.get('q')
        packages = model.CacheBinaryPackage.q().filter(model.CacheBinaryPackage.name.startswith(query))[:30]
        return '\n'.join(["%s|%s" % (package.name, package.description) for package in packages])

#--------------------------

def _process_screenshot(filehandle, package):
    """Analyse JPEG file through the Python Imaging Libary"""
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
    image_800_600, xsize, ysize = _resize(pil, 800, 600)
    # Create screenshot entry
    db_image_large = model.Screenshot(
        xsize=xsize,
        ysize=ysize,
        large=True,
        uploaderip=my.client_ip(),
        uploaderhash=my.client_cookie_hash()
        )

    # Resize to 160x120
    image_160_120, xsize, ysize = _resize(pil, 160, 120)
    # Create screenshot entry
    db_image_small = model.Screenshot(
        xsize=xsize,
        ysize=ysize,
        large=False,
        uploaderip=my.client_ip(),
        uploaderhash=my.client_cookie_hash()
        )

    db_pkg.screenshots.append(db_image_large)
    db_pkg.screenshots.append(db_image_small)
    db.commit()

    # Create the package's screenshots path if it does not exist yet
    # (As small images are saved into the same directory we just use db_image_large here)
    if not os.path.isdir(db_image_large.directory):
        log.debug("Create destination directory: %s" % db_image_large.directory)
        os.makedirs(db_image_large.directory)
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
