# -*- coding: utf-8 -*-
import logging
from debshots.lib.base import *
from pylons.controllers.util import Response
import os
try:
    import Image
except:
    import PIL.Image as Image
import StringIO
import paste
from paste.deploy.converters import asbool
from debshots.lib import my, validators
import formencode
from webhelpers.feedgenerator import Rss201rev2Feed

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

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

        # Only show packages with approved screenshots or the user's own screenshots
        # (JOINing reduces the packages to those which have corresponding screenshots)
        cookie_hash = my.client_cookie_hash()
        packages = packages.distinct().join('screenshots')
        packages = packages.filter(
            (model.Screenshot.approved==True)
            |
            (cookie_hash is not None and model.Screenshot.uploaderhash==cookie_hash)
            )
        packages = packages.options(model.orm.eagerload('screenshots'))

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

        c.packages = h.paginate.Page(packages,
            items_per_page=10,
            page=request.params.get('page',0),
            search=search,
            debtag=debtags_search,
            )

        return render('/packages/index.mako')

    @jsonify
    def pkglist(self):
        """Return list of packages as a JSON dictionary"""
        packages = model.Package.q()

        # Only show packages with approved screenshots or the user's own screenshots
        # (JOINing reduces the packages to those which have corresponding screenshots)
        packages = packages.join('screenshots')
        packages = packages.filter(model.Screenshot.approved==True)
        return {'packages':
            [
                {
                    'name': p.name,
                    'url': h.url_for('package', package=p.name, qualified=True),
                    'description': p.description,
                    'maintainer': p.maintainer,
                    'maintainer_email': p.maintainer_email,
                    'section': p.section,
                    'homepage': p.homepage,
                }
                for p in packages
            ]
        }

    @jsonify
    def screenshotslist(self):
        """Return list of screenshots as a JSON dictionary"""
        screenshots = model.newest_screenshots()

        return {'screenshots':
            [
                {
                    'name': s.package.name,
                    'url': h.url_for('package', package=s.package.name, qualified=True),
                    'description': s.package.description,
                    'maintainer': s.package.maintainer,
                    'maintainer_email': s.package.maintainer_email,
                    'section': s.package.section,
                    'homepage': s.package.homepage,
                    'version': s.version,
                    'small_image_url': h.url_for(s.small_image_url, qualified=True),
                    'large_image_url': h.url_for(s.large_image_url, qualified=True),
                }
                for s in screenshots
            ]
        }

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

        return render('/packages/show.mako')

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
            return self._image404(size)

        return self._image_by_path(file_path)

    def _image_by_package(self, package, size):
        """Return a thumbnail image or a dummy image for a certain package."""

        log.debug("Image requested. Size=%s. Package=%s.", size, package)

        # To save database queries we use memcached to store information
        # on whether a certain package has screenshots or not.
        cache_key = 'package_image:%s:%s' % (size, md5(package.encode('utf8')).hexdigest())
        file_path = g.cache.get(cache_key)

        if file_path is None:
            log.debug('Image information not found in memcached. Need to query database.')

            # No information found in memcached. Need to query the database.
            this_package = model.Package.q().filter_by(name=package).first()

            if not this_package or not this_package.screenshots:
                # The package doesn't exist or has no screenshots.
                file_path = 'DOES_NOT_EXIST' # needed because memcache libraries don't really differentiate False well
                #log.debug('No screenshot available for package: %s', package)
            else:
                # The package has screenshots. Store the path to the image
                # in memcached so next time we have the information readily available.
                file_path = this_package.screenshots[0].image_path(size)
                log.debug('Screenshot found at: %s', file_path)

            # Store the information in memcached. It is valid for 5 minutes.
            log.debug('Saving memcached entry for screenshot. Key: %s. Path: %s.',
                      cache_key, file_path)
            g.cache.set(cache_key, file_path, 300)
        else:
            log.debug('Image information found in memcached: %s', file_path)

        if file_path == 'DOES_NOT_EXIST' or not os.path.exists(file_path):
            # Image does not exist. Return a dummy image with response code 404 (Not found)
            return self._image404(size=size)
        else:
            # Image exists. Return it.
            log.debug("Serving static image from %s", file_path)
            if not os.path.isfile(file_path):
                log.warn("Image file %s not found" % file_path)
                return self._image404(size)
            return self._image_by_path(file_path)

    def image_by_id(self, id, size):
        """Return an image or None if there is no such image."""
        screenshot = model.Screenshot.q().get(id)

        # Make sure the screenshot database row is available
        if not screenshot:
            log.warn("Requested screenshot #%s which was not found in the database", id)
            return self._image404(size)

        # only show images that are approved (or for admins or owners)
        if not my.authorized_for_screenshot(screenshot):
            log.warn("User is not authorized to access screenshot #%s", id)
            return self._image404(size)

        file_path = screenshot.image_path(size)

        # Make sure the file on disk exists
        if not os.path.isfile(file_path):
            # The file is in the database but not on disk? Remove it from the database then.
            log.error("Screenshot #%s exists in database but is missing on disk at '%s'." % \
                      (screenshot.id, file_path))
            return self._image404(size)

        return self._image_by_path(file_path)

    def _image_by_path(self, image_path, status_code=None):
        """Return a PNG from disk.
        If status_code is set it defines the response code (e.g. 404)"""
        log.debug('Return image from path: %s', image_path)

        if status_code:
            # Don't use the Pylons default HTML response on 404 errors
            # (see also: http://pylonshq.com/docs/en/0.9.7/modules/middleware/#pylons.middleware.StatusCodeRedirect)
            request.environ['pylons.status_code_redirect'] = True
            response.status_int = status_code

        # Set headers
        response.headers['Content-Type'] = 'image/png'
        # make images cacheable
        response.headers['Cache-Control'] = 'public, max-age=86400'
        response.headers['Pragma'] = ''

        # If this applications runs behind an nginx with the xsendfile extension
        # enabled then we can just return an empty body and set the
        # X-Accel-Redirect header. nginx will then deliver the image directly
        # which is faster.
        if 'debshots.xsendfile' in config:
            response.headers[config['debshots.xsendfile']] = image_path
            log.debug('Telling the frontend web server to deliver the image directly from: %s', image_path)
            return ''

        image_file = open(image_path,'rb')
        image_data = image_file.read()
        image_file.close()
        return image_data

    def _image404(self, size):
        """Return a dummy image with response code 404

        'size' is either 'small' for a thumbnail or 'large' for the
        full-sized screenshot."""
        log.debug('Returning dummy image for size: %s', size)
        if size == 'small':
            file_name='dummy-thumbnail.png'
        elif size == 'large':
            file_name='dummy-screenshot.png'
        # Dummy image is found in public/images/ within the project directory
        image_path = os.path.join(
            config['pylons.paths']['static_files'],
            'images',
            file_name
            )
        return self._image_by_path(image_path, status_code=404)

    def thumbnail(self, package):
        """Return a thumbnail image of a certain package's screenshot"""
        return self._image_by_package(package=package, size='small')

    def screenshot(self, package):
        """Return a full-size image of a certain package's screenshot"""
        return self._image_by_package(package=package, size='large')

    def delete_screenshot(self, screenshot):
        this_screenshot = model.Screenshot.q().get(screenshot)
        if not this_screenshot:
            abort(404)

        package = this_screenshot.package

        # Make sure the user is allowed to delete the screenshot!
        if not my.authorized_for_screenshot(this_screenshot):
            abort(403, "I'm afraid I can't do that, Dave.")

        # Admins or the one who uploaded the screenshot is allowed to delete
        elif ('username' in session) or (my.client_cookie_hash() is not None and my.client_cookie_hash() == this_screenshot.uploaderhash):
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
            my.message("Screenshot for package <em>%s</em> already approved." % this_screenshot.package.name)
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
        log.debug('ajax_get_version_for_package(%s) -> %s' % (query, package.version))
        return { 'version' : package.version }

    def rss(self):
        """Return an RSS feed of the latest uploads"""
        feed = Rss201rev2Feed(
            title=u"screenshots.debian.net recent uploads",
            link='http://screenshots.debian.net',
            description=u"Recent uploads of screenshots to screenshots.debian.net",
            language=u"en",
        )

        # Show newest screenshot if available
        newest_screenshots = model.newest_screenshots()
        if newest_screenshots.count():
            # Return up to 30 screenshots in RSS feed
            for screenshot in newest_screenshots[:30]:
                feed.add_item(
                    title='Screenshot for %s (%s)' % (
                        screenshot.package.name, screenshot.package.description),
                    link=h.url_for('package', package=screenshot.package.name, qualified=True),
                    pubdate=screenshot.uploaddatetime,
                    description=h.tags.image(
                        url=h.url_for(screenshot.small_image_url, qualified=True),
                        alt=('Screenshot for package %s' % screenshot.package.name)
                    ),
                    #description=screenshot.package.name
                )

        response.content_type = 'application/rss+xml'
        return feed.writeString('utf-8')

#--------------------------


def _process_screenshot(filehandle, package, version):
    """Process the uploaded PNG file

    - resize to no larger than 800x600
    - resize (thumbnail) to no larger than 160x120
    - insert into database as Screenshot
    """
    try:
        image = Image.open(filehandle)
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
            image_copy.thumbnail(image_type['size'], Image.ANTIALIAS)
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
