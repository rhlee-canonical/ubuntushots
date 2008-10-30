# -*- coding: utf-8 -*-
import logging
from debshots.lib.base import *
import os
import PIL.Image
import StringIO

log = logging.getLogger(__name__)

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
        package = request.params.get('packagename')
        filename = request.params.get('file')
        if filename=='' or filename is None:
            # TODO: nicer error message
            return "No screenshot received."
        error = _process_screenshot(filename.file, package)
        if error:
            c.message=error
        else:
            log.info("Screenshot uploaded for package '%s'" % package)
            c.message="Screenshot for package '%s' uploaded successfully." % package

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
    db_image_large = model.Screenshot(xsize=xsize, ysize=ysize, large=True)

    # Resize to 160x120
    image_160_120, xsize, ysize = _resize(pil, 160, 120)
    # Create screenshot entry
    db_image_small = model.Screenshot(xsize=xsize, ysize=ysize, large=False)

    db_pkg.screenshots.append(db_image_large)
    db_pkg.screenshots.append(db_image_small)
    db.commit()

    dest_dir = os.path.join(config['debshots.images_directory'], package[0], package)
    if not os.path.isdir(dest_dir):
        log.debug("Create destination directory: %s" % dest_dir)
        os.makedirs(dest_dir)
    log.debug("Saving large image to %s" % dest_file_large)
    dest_file_large = os.path.join(config['debshots.images_directory'], package[0], package, str(db_image_large.id))
    image_800_600.save(dest_file_large, format='PNG')

    log.debug("Saving small image to %s" % dest_file_small)
    dest_file_small = os.path.join(config['debshots.images_directory'], package[0], package, str(db_image_small.id))
    image_160_120.save(dest_file_small, format='PNG')

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
