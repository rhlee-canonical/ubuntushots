"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    # Show approved screenshots. It's faster to serve /screenshots from the
    # web server as static files instead.
    map.connect('image', '/screenshots/:package_inital/:package/:(id)_:size.png',
        controller='packages', action='static_image',
        requirements={'id': r'\d+', 'size': '(small|large)'})

    map.connect('unapproved_image', '/image/:(id)_:size.png',
        controller='packages', action='image_by_id',
        requirements={'id': r'\d+', 'size': '(small|large)'})

    # Start page
    map.connect('start', '/', controller='start', action='index')

    # Packages view (list of packages with screenshots sorted by name)
    map.connect('packages', '/packages', controller='packages', action='index')

    # List of packages with screenshots
    map.connect('packageslist', '/json/packages', controller='packages', action='pkglist')
    map.connect('screenshotslist', '/json/screenshots', controller='packages', action='screenshotslist')

    # View for logged-in administrators to approve or delete uploaded screenshots
    map.connect('moderate', '/packages/moderate', controller='packages', action='moderate')

    # Show upload form
    map.connect('upload', '/upload', controller='packages', action='upload', package=None)
    # Deprecated link to the guidelines (now included in the upload page)
    map.connect('guidelines', '/guidelines', controller='start', action='guidelines')
    # Handle the actual upload
    map.connect('upload', '/upload/:package', controller='packages', action='upload')

    # Process upload form
    map.connect('uploadfile', '/uploadfile', controller='packages', action='uploadfile')

    # Admin login form
    map.connect('login', '/login', controller='start', action='login')

    # Admin logout form
    map.connect('logout', '/logout', controller='start', action='logout')

    # Details about a package
    map.connect('package', '/package/:package', controller='packages', action='show')

    # Direct link to a thumbnail image of a certain package
    # (shows a dummy 160x120 pixel large along with response code 404)
    map.connect('thumbnail', '/thumbnail/:package', controller='packages', action='thumbnail')
    # URL used by the Ubuntu software center
    map.connect('thumbnail-404', '/thumbnail-404/:package', controller='packages', action='thumbnail')
    # Same for the large image
    map.connect('screenshot', '/screenshot/:package', controller='packages', action='screenshot')
    # URL used by the Ubuntu software center
    map.connect('screenshot-404', '/screenshot-404/:package', controller='packages', action='screenshot')

    # Action to delete a screenshot (admin-only) or request its removal (users)
    map.connect('delete_screenshot', '/delete_screenshot/:screenshot',
        controller='packages', action='delete_screenshot')

    # Action to approve a screenshots (admin-only)
    map.connect('approve_screenshot', '/approve_screenshot/:screenshot',
        controller='packages', action='approve_screenshot')

    # Action to remove the 'markedfordelete' flag (admin-only)
    map.connect('keep_screenshot', '/keep_screenshot/:screenshot',
        controller='packages', action='keep_screenshot')

    map.connect('rss', '/rss', controller='packages', action='rss')

    # Generic controllers
    #map.connect(':controller/:action/:id')
    map.connect('/:controller/:action')
    #map.connect('*url', controller='template', action='view')

    #map.connect('/{controller}/{action}')
    #map.connect('/{controller}/{action}/{id}')


    return map

