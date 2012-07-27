#!/usr/bin/python2
# Author: Ross Delinger
# Description: Uses Gevent and static to serve files in a directory
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer
import sys
import os
import mimetypes
from collections import defaultdict

def get_file_stats(path):
    files = []
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    type_dict = defaultdict(list)
    map(lambda f: type_dict[mimetypes.guess_type(f)[0]].append(1), files)
    for key in type_dict:
        type_dict[key] = sum(type_dict[key])
    file_stats = sorted(type_dict.items(), key=lambda i: i[1], reverse=True)
    formatted_stats = map(lambda stat: "<li>{0}: {1}</li>".format(stat[0],
        stat[1]),file_stats)
    return '<html><ul>' + '\n'.join(formatted_stats) + '</ul></html>'

class CombinedApp(object):
    def __init__(self, static_app, static_path):
        self.static_app = static_app
        self.static_path = static_path
    def __call__(self, environ, start_response):
        if environ['PATH_INFO'] == "/":
            start_response('200 OK', [('Content-Type', 'text/html')])
            return get_file_stats(self.static_path)
        else:
            return self.static_app(environ, start_response)

def main():
    """
    Main function which gets the path from the cl arguments
    and then starts the gevent wsgiserver with the static.cling app
    """

    try:
        path = sys.argv[1]
    except:
        path = os.getcwd()
    print "Serving files for {0}".format(path)
    import static
    static_app = static.Cling(path)
    wsgi = WSGIServer(("localhost", 8081),
            application = CombinedApp(static_app, path))
    try:
        wsgi.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down"
        return

if __name__ == "__main__":
    main()
