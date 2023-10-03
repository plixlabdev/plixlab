import tornado.ioloop
import tornado.web
import os
import json
import webbrowser
from tornado import autoreload
from tornado import websocket
#from plix import Presentation

# List to store active WebSocket connections
active_sockets = []

class ReloadWebSocketHandler(websocket.WebSocketHandler):
    def open(self):
        active_sockets.append(self)

    def on_close(self):
        active_sockets.remove(self)


data_to_serve = None

class NoCacheHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '0')

    #class MainHandler(tornado.web.RequestHandler):
    def get(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(script_dir, 'index.html')
        with open(index_path, 'r') as f:
            self.write(f.read())

def set_default_headers(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '0')

class DataHandler(tornado.web.RequestHandler):
    def get(self):
        # Set the response header to be JSON format
        self.set_header("Content-Type", 'application/json')
        
        # Write the data as JSON
        self.write(json.dumps(data_to_serve))

class PingHandler(tornado.web.RequestHandler):
    def get(self):

        self.write("pong")

class ShareHandler(tornado.web.RequestHandler):
    def get(self):

        #Share and get the URL-------
        url = Presentation.read(data_to_serve).push(verbose=False)

        #Send back the url to the client
        self.write(url)

def make_app():
    return tornado.web.Application([
        (r"/",NoCacheHandler),
        (r"/ping", PingHandler),
        (r"/share", ShareHandler),
        (r"/data", DataHandler),
        (r"/reload", ReloadWebSocketHandler),
        (r"/(render.js|styles.css|code.js)", tornado.web.StaticFileHandler, {"path": os.path.dirname(os.path.abspath(__file__))})
    ])

def send_reload():
    """This will be called before the server restarts."""
    for socket in active_sockets:
        socket.write_message("reload")


def run(data):
    global data_to_serve
    data_to_serve = data

    app = make_app()
    app.listen(8888)

    # Check if the environment variable is set
    if not os.environ.get("BROWSER_OPENED"):
        # Automatically open the browser
        webbrowser.open("http://localhost:8888")
        # Set the environment variable
        os.environ["BROWSER_OPENED"] = "True"

    # Add the hook to send "reload" message to active sockets before restart
    autoreload.add_reload_hook(send_reload)

    autoreload.start()
 
    tornado.ioloop.IOLoop.current().start()
