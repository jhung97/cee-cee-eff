from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import os
 
def send_data_to_server():
         
    image_filename = os.path.basename("1200 test")
 
    multipart_form_data = {
        'image': (image_filename, open("./sample-001200.png", 'rb')),
    }
 
    response = requests.post('localhost:8000',
                             files=multipart_form_data)
 
    print(response.status_code)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

        #send_data_to_server()

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()

