import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

PAGE="""\
<html>
<style>
img {
  display: inline-block;
  position: absolute;
  width: 50%;
  height: 50%;
}
table {
  table-layout: fixed;
  width: 50%;
}
td {
  width: 25%;
} 
button {
  font-size: 20px;
  width: 100%;
}
.button_arrow {
  background-color: #4CAF50;
}
.button_fire {
  background-color: #f44336;
}
iframe{
  display: none;
}
</style>
<head>
<title>Pesky Medeling Co-Worker Repellant</title>
</head>
<body>
<script>
function left() {
  let xhr = new XMLHttpRequest();
  xhr.open('post', 'left');
  xhr.send();
}
function right() {
  let xhr = new XMLHttpRequest();
  xhr.open('post', 'right');
  xhr.send();
}
function up() {
  let xhr = new XMLHttpRequest();
  xhr.open('post', 'up');
  xhr.send();
}
function down() {
  let xhr = new XMLHttpRequest();
  xhr.open('post', 'down');
  xhr.send();
}
function fire() {
  let xhr = new XMLHttpRequest();
  xhr.open('post', 'fire');
  xhr.send();
}
</script>
<h1>Pesky Medeling Co-Worker Repellant</h1>
<table>
  <tr>
    <th></th>
    <th>
    <form action="javascript:up();" method="post">
      <button type="submit" class="button_arrow" type="button">&uarr;</button>
    </form>
    </th>
    <th></th>
  </tr>
  <tr>
    <th>
    <form action="javascript:left();" method="post">
      <button type="submit" class="button_arrow" type="button">&larr;</button>
    </form>
    </th>
    <th>
    <form action="javascript:fire();" method="post">
      <button type="submit" class="button_fire" type="button">TERMINATE!!!</button>
    </form>
    <th>
    <form action="javascript:right();" method="post">
      <button type="submit" class="button_arrow" type="button">&rarr;</button>
    </form>
    </th>
  </tr>
  <tr>
    <th></th>
    <th>
    <form action="javascript:down();" method="post">
      <button type="submit" class="button_arrow" type="button">&darr;</button>
    </form>
    </th>
    <th></th>
  </tr>
</table>
<br>
<img src="stream.mjpg" width="640" height="480"/>
<img src="crosshairs.png" width="640" height="480"/>
</body>
<iframe name="left"></iframe>
<iframe name="right"></iframe>
<iframe name="fire"></iframe>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        f = open('crosshairs.png', 'rb')
        self.crosshairs = f.read()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == '/left':
            self.send_response(200)
            print("left")
        if self.path == '/right':
            self.send_response(200)
            print("right")
        if self.path == '/up':
            self.send_response(200)
            print("up")
        if self.path == '/down':
            self.send_response(200)
            print("down")
        if self.path == '/fire':
            self.send_response(200)
            print("FIRE!")
        else:
            self.send_error(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/crosshairs.png':
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.send_header('Content-Length', len(self.crosshairs))
            self.end_headers()
            self.wfile.write(self.crosshairs)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()

