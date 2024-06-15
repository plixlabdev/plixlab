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
        (r"/share", ShareHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")}),
        (r"/assets/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "assets")}),
        (r"/data", ReloadWebSocketHandler,{"data_provider": data_provider}),
        (r"/(render.js|styles.css|navigation.js|models.js|load.js|local_only.js)", tornado.web.StaticFileHandler, {"path": os.path.dirname(os.path.abspath(__file__))})
    ])



def set_default_headers(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '0')


class ShareHandler(tornado.web.RequestHandler):
    def get(self):
        
        url = push_data(data_to_serve,verbose=False)

        #Send back the url to the client
        self.write(url)



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

         old_data = {}        
         
         if os.path.isfile('./.cache') and not(self.first_connection):
            with open('./.cache','r') as f:
                old_data = json.load(f)

         data_to_serve = self.data_provider
   
         patch = list(jsonpatch.JsonPatch.from_diff(old_data,data_to_serve))
         if len(patch) > 0:
            
            #-------------- 
            self.write_message(msgpack.packb(patch),binary=True)

            #self.write_message(json.dumps({'patch':patch}))

            #with open('./.cache','w') as f:
            #   json.dump(data_to_serve,f)

def run(data_provider):

        app = make_app(data_provider)
        app.listen(8888)

        # Check if the environment variable is set
        if not os.environ.get("BROWSER_OPENED"):
         webbrowser.open("http://localhost:8888")
         os.environ["BROWSER_OPENED"] = "True"

        # Add the hook to send "reload" message to active sockets before restart
        autoreload.start()
 
        io_loop = tornado.ioloop.IOLoop.current()
      

        io_loop.start()



        
