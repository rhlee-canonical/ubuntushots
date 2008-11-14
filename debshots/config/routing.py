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

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('error/:action/:id', controller='error')

    # CUSTOM ROUTES HERE
    map.connect('image', '/screenshots/:package_inital/:package/:(id)_:size.png',
        requirements={'id': r'\d+', 'size': '(small|large)'})
    map.connect('unapproved_image', '/image/:(id)_:size.png',
        controller='packages', action='image',
        requirements={'id': r'\d+', 'size': '(small|large)'})
    map.connect('start', '', controller='start', action='index')
    map.connect('packages', '/packages', controller='packages', action='index')
    map.connect('moderate', '/packages/moderate', controller='packages', action='moderate')
    map.connect('upload', '/upload/:package', controller='packages', action='upload', package=None)
    map.connect('uploadfile', '/uploadfile', controller='packages', action='uploadfile')
    map.connect('guidelines', '/guidelines', controller='start', action='guidelines')
    map.connect('login', 'login', controller='start', action='login')
    map.connect('logout', 'logout', controller='start', action='logout')
    map.connect('package', 'package/:package', controller='packages', action='show')
    map.connect('thumbnail', 'thumbnail/:package', controller='packages', action='thumbnail')
    map.connect('delete_screenshot', '/delete_screenshot/:screenshot',
        controller='packages', action='delete_screenshot')
    map.connect('approve_screenshot', '/approve_screenshot/:screenshot',
        controller='packages', action='approve_screenshot')
    map.connect('keep_screenshot', '/keep_screenshot/:screenshot',
        controller='packages', action='keep_screenshot')
    map.connect('login', '/login', controller='start', action='login')
    map.connect('logout', '/logout', controller='start', action='logout')
    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='view')




    return map
