import http.server
import json
import socketserver
from io import BytesIO
import cgi

PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):

    def run_name(self, name):
        print(f'running {name}...')

    def send_my_headers(self):
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.end_headers()

    def only_json_response(self, content_type):
        self.send_response(400)
        self.send_header('content-type', content_type)
        self.end_headers()
        response = BytesIO()
        response.write(b'ALLOWED ONLY JSON!\nSend as JSON.')
        self.wfile.write(response.getvalue())
        return

    def received_response(self, data):  # эта функция возвращает ответ на POST метод
        self.send_my_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    async def do_POST(self):
        content_type, pdict = cgi.parse_header(self.headers.get('content-type'))  # получаем тип запроса
        if content_type != 'application/json':  # проверка типа на JSON
            self.only_json_response(content_type)

        # если проходит проверку, выполняется следующий код:
        else:
            length = int(self.headers.get('content-length'))  # получаем размер запроса
            post_data = json.loads(self.rfile.read(length))   # содержимое запроса
            self.received_response(post_data)


my_handler = Handler

try:
    with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), my_handler) as httpd:
        print(f"Starting at http://127.0.0.1:{PORT}\nNow you can send POST request.\nUse POSTMAN or curl.")
        httpd.serve_forever()

except KeyboardInterrupt:
    httpd.shutdown()
    print("Stopping server")
    httpd.server_close()
