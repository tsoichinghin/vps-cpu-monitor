import psutil
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/cpu':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            cpu_usage = get_cpu_usage()
            self.wfile.write(str(cpu_usage).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def start_server():
    cpu_usage = get_cpu_usage()
    def update_cpu_usage():
        nonlocal cpu_usage
        while True:
            cpu_usage = get_cpu_usage()
            time.sleep(5)
            
    threading.Thread(target=update_cpu_usage, daemon=True).start()
    server_address = ('', 3003)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting server on port 3003...')
    httpd.serve_forever()

if __name__ == '__main__':
    start_server()
