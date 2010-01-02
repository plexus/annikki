"""Routes configuration
"""

from pylons import config
from routes import Mapper

"""
Annikki is composed of two seperate WSGI applications, one for the
website, one for the API that is called by the Anki plugin. This is
done so we can have a more minimal middleware stack for the plugin
controllers.

make_map : routes map for the website
make_api_map : routes map for the API
"""

def make_map():
    controller_dir = config['pylons.paths']['controllers']
    map = Mapper(directory = controller_dir, always_scan=config['debug'])
    map.minimization = False

    #keep these first
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')


    map.connect('/', controller='main')

    map.connect('/signup', controller='user', action='signup')
    map.connect('/user/{user}', controller='user', action='profile')

    #keep these last
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map


def make_api_map():
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.minimization = False

    map.connect('/{action}', controller='api')

    #map.connect('/{controller}/{action}')
    #map.connect('/{controller}/{action}/{id}')

    return map
