from http.server import BaseHTTPRequestHandler
from info_parse import MultisemanticPacket
import time
from pose_task import PoseTask
import json

class MultisemanticHTTPServerHandler(BaseHTTPRequestHandler):
    __pose_task = PoseTask()
    def set_html_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def set_json_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    # the do_GET name is mandatory
    def do_GET(self):
        self.set_html_headers()
        self.wfile.write(bytes("<html><body><h1>hello</h1></body></html>", "utf-8"))

    def do_POST(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        (json_packet, img) = MultisemanticPacket.info_parse(self.data_string)

        packet = {
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
            'user': json_packet['user'],
            'mode': json_packet['mode'],
            'function': json_packet['function'],
            'result': '',
        }

        if img.any():
            result = MultisemanticHTTPServerHandler.__pose_task.run(img)
            packet['result'] = result.tolist()

        self.set_json_headers()
        self.wfile.write(bytes(json.dumps(packet), "utf-8"))
