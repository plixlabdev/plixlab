import webbrowser
from tornado import autoreload
from tornado import websocket
import tornado.ioloop
import tornado.web
import os
import json,jsonpatch
import msgpack

def make_app(data_provider):
    return tornado.web.Application([
        (r"/",NoCacheHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")}),
        (r"/assets/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "assets")}),
        (r"/data", ReloadWebSocketHandler,{"data_provider": data_provider}),
         (r"/events", ReadySSEHandler),  # SSE handler for sending "ready"

    ])
class ReadySSEHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "text/event-stream")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")

    async def get(self):
        """
        Handle SSE connections and send a 'ready' signal.
        Gracefully handle server reload and disconnections.
        """
        global active_sse_connections
        active_sse_connections.append(self)

        try:
            print("New SSE connection established.")

            # Send the "ready" message
            self.write("retry: 2000\n")  # Retry every 3 seconds
            self.write("data: ready\n\n")  # SSE-compliant format
            self.flush()  # Ensure the message is sent immediately

            # Keep the connection alive
            while True:
                await tornado.gen.sleep(10)  # Prevent immediate disconnection
        except tornado.iostream.StreamClosedError:
            print("SSE client disconnected.")
        except Exception as e:
            print(f"Unexpected error in SSE handler: {e}")
        finally:
            print("SSE connection closed.")
            active_sse_connections.remove(self)
            self.finish()


def set_default_headers(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '0')


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


class ReloadWebSocketHandler(websocket.WebSocketHandler):

    def open(self):
        first_connection_param = self.get_argument('isFirstConnection', 'false')
        self.first_connection = first_connection_param.lower() == 'true'
        print(f"First connection: {self.first_connection}")
        self.send_data_to_client()

    def initialize(self, data_provider):
        self.data_provider = data_provider
       
    def on_message(self, message):
        pass


    def send_data_to_client(self):
         #We send the patch to the client

        #  old_data = {}
        #  if os.path.isfile('./.cache'):
        #     with open(".cache", "rb") as file:
        #        old_data = msgpack.unpackb(file.read())
        
        #  # Write the packed data to a file
        #  with open(".cache", "wb") as file:
        #   file.write(msgpack.packb(self.data_provider))

         
        #  patch = list(jsonpatch.JsonPatch.from_diff(old_data,self.data_provider))
        #  for p in patch:
        #      print(p['op'] + ' ' +  p['path'])
    

        # print('Sending data to client...')

       #print(self.data_provider)
       

       self.write_message(msgpack.packb(self.data_provider),binary=True)

         
def run(data_provider):
    print('Starting Tornado server...')
    port = 8889
    app = make_app(data_provider)
    app.listen(port)

    # Open the browser only on the first run
    if not os.environ.get("BROWSER_OPENED"):
        webbrowser.open(f"http://localhost:{port}")
        os.environ["BROWSER_OPENED"] = "True"

    # Start autoreload to monitor file changes
    

    autoreload.add_reload_hook(lambda: print("Server is reloading..."))
    autoreload.add_reload_hook(lambda: cleanup_connections())
    autoreload.add_reload_hook(lambda: tornado.ioloop.IOLoop.current().stop())
    autoreload.start()

    io_loop = tornado.ioloop.IOLoop.current()
    print(f"Server running at http://localhost:{port}")
    io_loop.start()




# Track active connections
active_sse_connections = []

def cleanup_connections():
    """
    Clean up active SSE connections during server reload.
    """
    print("Cleaning up active SSE connections...")
    for connection in active_sse_connections:
        try:
            connection.finish()
        except Exception as e:
            print(f"Error while closing SSE connection: {e}")
    active_sse_connections.clear()


        

        # if os.path.isfile('./.cache') and not(self.first_connection):

        #    with open(".cache", "rb") as file:
        #       old_data = msgpack.unpackb(file.read())
        # else:
        #       old_data = {}             

         # Write the packed data to a file
        # with open(".cache", "wb") as file:
        #  file.write(msgpack.packb(self.data_provider))


         
         #patch = list(jsonpatch.JsonPatch.from_diff(old_data,self.data_provider))
         #for p in patch:
         #    print(p['op'] + ' ' +  p['path'])
    
         #print('here')
         #self.data_provider
          #if len(patch) > 0: