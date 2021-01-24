#  coding: utf-8
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s" % self.data)

        # decode the data
        decoded_data = self.data.decode("utf-8").split("\r\n")

        http_method, path, protocol = decoded_data[0].split(" ")

        # throw 405 if it's not a GET request
        if http_method != "GET":
            self.request.sendall(bytearray(
                "HTTP/1.1 405 Method Not Allowed", 'utf-8'))

        else:
            print(path)
            if path == '/':
                path = "/index.html/"

            # Getting the full path of file
            # taken from Russell Dias https://stackoverflow.com/users/322129/russell-dias
            # From StackOverflow
            # From https://stackoverflow.com/a/5137509
            full_path = os.path.realpath(os.getcwd() + '/www' + path)

            # CSS Mimetype
            # taken from https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types#textcss
            # From Developer Mozilla
            if ".css" in path or '.html' in path:
                if os.path.exists(full_path):
                    try:
                        # Reading a file
                        # Taken from alKid https://stackoverflow.com/users/2106009/aikid
                        # From StackOverflow
                        # From https://stackoverflow.com/a/19508772
                        with open(full_path, 'r') as f:
                            data = f.read()

                        if ".css" in path:
                            content_type = "text/css"
                        else:
                            content_type = "text/html"

                        self.request.sendall(bytearray(
                            f"HTTP/1.1 200 OK\r\n\r\nContent-Type: {content_type}\r\n" + data, 'utf-8'))
                    except:
                        self.request.sendall(bytearray(
                            f"HTTP/1.1 301 Moved Permanently\r\n\r\nLocation: {path}/", 'utf-8'))
                else:
                    self.request.sendall(bytearray(
                        "HTTP/1.1 404 Not Found", 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
