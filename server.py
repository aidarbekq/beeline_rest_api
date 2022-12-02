import http.server
import json
import os
from io import BytesIO
import cgi
from datetime import datetime
import re
from threading import Thread
import pause

PORT = 8000


def printing_name():
    """Функция отложенного исполнения"""
    with open(f"post_json_data_.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        json_time = data['time']  # получаем данные "time" отправленных клиентами
        times = re.split('-| |:', json_time)   # преобразовываем данные 'time' в datetime(python) формат
        schedule_time = datetime(int(times[0]), int(times[1]), int(times[2]), int(times[3]), int(times[4]))
        pause.until(schedule_time)
    print(data['name']) # вывод "name" в консоль


class Handler(http.server.SimpleHTTPRequestHandler):

    def send_my_headers(self):
        """Функция для отправки хэдеров"""
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.end_headers()

    def only_json_response(self, content_type):
        """Если клиент отправляет не JSON, выполняется эта функция"""
        self.send_response(400)
        self.send_header('content-type', content_type)
        self.end_headers()
        response = BytesIO()
        response.write(b'ALLOWED ONLY JSON!\nSend as JSON.')
        self.wfile.write(response.getvalue())
        return

    def received_response(self, data):
        """эта функция возвращает ответ на POST метод"""
        self.send_my_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_POST(self):
        """POST метод"""
        content_type, pdict = cgi.parse_header(self.headers.get('content-type'))  # получаем тип запроса
        if content_type != 'application/json':  # проверка типа на JSON
            self.only_json_response(content_type)

        # если проходит проверку, выполняется следующий код:
        else:
            length = int(self.headers.get('content-length'))  # получаем размер запроса
            post_data = json.loads(self.rfile.read(length))  # содержимое запроса
            if post_data:
                self.received_response(post_data)
                with open("post_json_data_.json", "w") as outfile:
                    json.dump(post_data, outfile)
                if os.path.exists(f"post_json_data_.json"):
                    thread = Thread(target=printing_name, daemon=True)
                    thread.start()


my_handler = Handler


try:
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), my_handler) as httpd:
        print(f"Starting at http://127.0.0.1:{PORT}\nNow you can send POST request.\nCTRL+C to STOP.")
        httpd.serve_forever()   # запуск сервера


except KeyboardInterrupt:  # CTRL+C
    httpd.shutdown()
    print("Stopping server")
    httpd.server_close()


