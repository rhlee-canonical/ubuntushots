# -*- coding: utf-8 -*-
import logging
from debshots.lib.base import *
import os
import PIL.Image
import StringIO

log = logging.getLogger(__name__)

class PackagesController(BaseController):

    #def index(self):
    #    """Show a list of packages with screenshots"""
    #    packages = model.Package.q()
    #    c.packages = h.paginate.Page(packages,
    #        page=int(request.params.get('page_nr')))
    #    return render('/packages/index.mako')

    def upload(self):
        """Show package upload dialog"""
        return render('/packages/upload.mako')

    def uploadfile(self):
        """Deal with uploaded screenshot"""
        package = request.params.get('packagename')
        filename = request.params.get('file')
        if filename=='' or filename is None:
            # TODO: nicer error message
            return "No screenshot received."
        error = _process_screenshot(filename.file, package)
        if error:
            return "Crap: %s" % error
            # TODO...
        else:
            log.info("Screenshot uploaded for package '%s'" % package)

        return render('/packages/upload.mako')

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

    xsize, ysize = pil.size
    xsize = float(xsize)
    ysite = float(ysize)

    if xsize==800 and ysize==600:
        log.debug("Image is already 800x600 - no conversion necessary")
    # Image too wide for a 800/600 ratio?
    elif xsize/ysize > 800.0/600.0:
        resize_factor = 800/xsize
        log.debug("Image too wide for 800x600. Resizing by %f")
        xsize_large = 800
        ysize_large = int(ysize*resize_factor)
        xsize_small = 160
        ysize_small = int(ysize*resize_factor/5)
    # Image too high for a 800/600 ratio?
    else:
        resize_factor = 600/ysize
        log.debug("Image too high for 800x600.")
        xsize_large = xsize*resize_factor
        ysize_large = 600
        xsize_small = ysize*resize_factor/5
        ysize_small = 120

    log.debug("Large image will be resized to: %s x %s" % (xsize_large, ysize_large))
    log.debug("Small image will be resized to: %s x %s" % (xsize_small, ysize_small))
    image_800_600 = pil.resize((xsize_large, ysize_large), PIL.Image.ANTIALIAS)
    image_160_120 = pil.resize((xsize_small, ysize_small), PIL.Image.ANTIALIAS)

    # Is there a database entry for this package already?
    log.debug("Fetch package entry from database for package '%s'" % package)
    db_pkg = model.Package.q().filter_by(name=package).first()
    if not db_pkg: # otherwise create one
        log.debug("No package entry found. Creating a new one.")
        db_pkg = model.Package(name=package)
        db.save(db_pkg)

    # Create screenshot entry
    db_image_large = model.Screenshot(xsize=xsize_large, ysize=ysize_large, large=True)
    db_image_small = model.Screenshot(xsize=xsize_small, ysize=ysize_small, large=False)
    db_pkg.screenshots.append(db_image_large)
    db_pkg.screenshots.append(db_image_small)
    db.commit()

    dest_dir = os.path.join(config['debshots.images_directory'], package[0], package)
    if not os.path.isdir(dest_dir):
        log.debug("Create destination directory: %s" % dest_dir)
        os.makedirs(dest_dir)
    dest_file_large = os.path.join(config['debshots.images_directory'], package[0], package, str(db_image_large.id))
    dest_file_small = os.path.join(config['debshots.images_directory'], package[0], package, str(db_image_small.id))
    log.debug("Saving large image to %s" % dest_file_large)
    log.debug("Saving small image to %s" % dest_file_small)
    # Save large and small version to disk
    image_800_600.save(dest_file_large, format='PNG')
    image_160_120.save(dest_file_small, format='PNG')
    return None # Success
