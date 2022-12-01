import http.server
import socketserver
from io import BytesIO

PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(201)
        self.send_header('Content-type', 'text')
        self.end_headers()
        response = BytesIO()
        response.write(b'\nyou send this text: ')
        response.write(post_data)
        self.wfile.write(response.getvalue())


my_handler = Handler

try:
    with socketserver.TCPServer(("127.0.0.1", PORT), my_handler) as httpd:
        print(f"Starting at http://127.0.0.1:{PORT}\nNow you can send POST request")
        httpd.serve_forever()

except KeyboardInterrupt:
    httpd.shutdown()
    print("Stopping server")
    httpd.server_close()
