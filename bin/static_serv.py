#!/usr/bin/python2
# Author: Ross Delinger
# Description: Uses Gevent and static to serve files in a directory
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer
import sys
import os

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
    wsgi = WSGIServer(("localhost", 8081), application = static_app)
    try:
        wsgi.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down"
        return

if __name__ == "__main__":
    main()
