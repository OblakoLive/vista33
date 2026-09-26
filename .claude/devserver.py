import http.server
import os

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path.startswith('/__save'):
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            target = self.path.split('?', 1)[1] if '?' in self.path else 'upload.bin'
            target = os.path.normpath(target).lstrip('\\/')
            if '..' in target.split(os.sep):
                self.send_response(400); self.end_headers(); return
            full = os.path.join(os.getcwd(), target)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'wb') as f:
                f.write(body)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(f'saved {len(body)} bytes to {target}'.encode())
        else:
            self.send_response(404); self.end_headers()

if __name__ == '__main__':
    http.server.test(HandlerClass=Handler, port=8420)
