import os
from http.server import HTTPServer, CGIHTTPRequestHandler


class webServer(object):
    def __init__(self):
        print('webserver class is called')
        self.startWebServer()


    def startWebServer(self):
        # Make sure the server is created at current directory
        print('starting web server')
        os.chdir('./temp/')
        # Create server object listening the port 8001
        server_object = HTTPServer(server_address=('127.0.0.1', 8001), RequestHandlerClass=CGIHTTPRequestHandler)
        # Start the web server
        server_object.serve_forever()

