# ----------------------------------------------------------------- #
#  File   : __init__.py
#  Author : peach
#  Date   : 8 July 2019
# ----------------------------------------------------------------- #

import tsl.configuration
import tsl.server.api
import tsl.util.log
import tsl.util.path
import tsl.util.env

import http.server
import time
import json

_ROOT_DIRECTORY = tsl.util.env.get_environment_variable('APP_ROOT')
_ENABLE_LOGGING = tsl.configuration.val('SERVER_ENABLE_LOGGING')


class Server:

    def __init__(self, hostName, portNumber):
        self.hostName = hostName
        self.portNumber = portNumber
        self.server_class = http.server.HTTPServer
        self.httpd = self.server_class(
            (self.hostName, self.portNumber), RequestHandler)

    def start(self):
        tsl.util.path.cd(_ROOT_DIRECTORY)
        tsl.util.log.info(
            "{} - Server Started - {}:{}".format(time.asctime(), self.hostName, self.portNumber))
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        self.stop()

    def stop(self):
        # Close Down Server
        self.httpd.server_close()
        tsl.util.log.info(
            "{} - Server Stopped - {}:{}".format(time.asctime(), self.hostName, self.portNumber))


class RequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.is_api_request():
            self.handle_api_request()
            return

        # Fix the root directory issue.
        if self.path == "/":
            self.path = "/html/index.html"

        # Serve normal files.
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # Make sure that the API was used. If not, send a 404.
        if self.is_api_request():
            self.handle_api_request()
            return

        self.send_response(400)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write("Invalid POST request".encode())

    def is_api_request(self):
        return (self.path.find('/api/') == 0)

    def handle_api_request(self):
        data = None
        method = self.command
        endpoint = self.path

        data_length_str = self.headers['Content-Length']
        if data_length_str:
            data_length = int(data_length_str)
            data_json = self.rfile.read(data_length).decode()
            data = json.loads(data_json)

        api_result = tsl.server.api.handle_request(method, endpoint, data)
        self.send_response(api_result.status)
        self.send_header("Content-type", api_result.mimetype)
        self.end_headers()
        self.wfile.write(api_result.data.encode())

    def log_message(self, *args):
        if (_ENABLE_LOGGING):
            http.server.SimpleHTTPRequestHandler.log_message(self, *args)
        return