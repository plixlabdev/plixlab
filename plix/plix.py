import os
import requests
import base64
import io
import matplotlib.pyplot as plt
import json
import plotly.io as pio
from .utils import get_style,get_youtube_thumbnail,process_plotly,fig_to_base64,load_icon,encode_image_to_base64
from plotly.io import from_json as json_to_plotly
#from .serve import run 
from .shape import run as shape
import tornado.ioloop
import tornado.web
import os
import json
import webbrowser
from tornado import autoreload
from tornado import websocket
import numpy as np
from . import Bibliography

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the style file
style_path = os.path.join(script_dir, 'assets', 'mpl_style')
# Use the style
plt.style.use(style_path)


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

          
def push_data(content,local=False,token=None,verbose=True):

      #Get token
      if not token: token = './computing_together.txt'
      with open(token,'r') as f:
           refresh_token = f.read()

      if local:
       url_prefix = 'http://127.0.0.1:5000/presentation'
       url ='http://127.0.0.1:5001/computo-306914/us-central1/upload'
      else: 
       url_prefix = 'https://computo-306914.web.app/presentation'
       url = 'https://upload-whn4gonsea-uc.a.run.app'


      # Get SignedURL--------------------------
      headers = {
      'Authorization': f'Bearer {refresh_token}',
      'Content-Type': 'application/json'
      }
      output = requests.post(url, json={"title": content['title']}, headers=headers).json()
      signedURL = output['signedUrl']
      #----------------------------------------
    

      #Upload data
      response = requests.put(signedURL, headers={"Content-Type": "application/json"}, json=content)

      url = url_prefix + '/' +  output['url']
      #Print URL
      if verbose:
       print(url)

      return url 

def set_default_headers(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '0')

class DataHandler(tornado.web.RequestHandler):
    def get(self):
        # Set the response header to be JSON format
        self.set_header("Content-Type", 'application/json')
      
        # Write the data as JSON
        print(len(data_to_serve['data']))
        self.write(json.dumps(data_to_serve))

class PingHandler(tornado.web.RequestHandler):
    def get(self):

        self.write("pong")

class ShareHandler(tornado.web.RequestHandler):
    def get(self):
        
        url = push_data(data_to_serve,verbose=False)

        #Send back the url to the client
        self.write(url)



def make_app():
    return tornado.web.Application([
        (r"/",NoCacheHandler),
        (r"/ping", PingHandler),
        (r"/share", ShareHandler),
        (r"/data", DataHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")}),
        (r"/assets/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "assets")}),
        (r"/reload", ReloadWebSocketHandler),
        (r"/(render.js|styles.css|code.js)", tornado.web.StaticFileHandler, {"path": os.path.dirname(os.path.abspath(__file__))})
    ])

def send_reload():
    """This will be called before the server restarts."""
    for socket in active_sockets:
        socket.write_message("reload")


        
class Presentation():
   """Class for presentations"""

   def __init__(self,slides=[],title='untitled'):


         self.title = title

         self.content = [slide.content for slide in slides]   
         
         self.animation = [slide.animation for slide in slides]

   #@classmethod
   #def read(cls,data):
   #    """Import presentation"""   

   #    #prepare content
       #slides = [Slide(content=content) for i,content in enumerate(data)]

   #    a = cls(); 
   #    a.content = data['data'] 
   #    a.animation = data['animation'] 
   #    return a

   
   def slide(self,slide):  
         """Add a slide"""

         self.content.append(slide.content) 
         self.animation.append(slide.animation) 

         return slide



   def _render_animation(self):

        #Add IDs to Slides
        for s,slide in enumerate(self.content):
           slide['id'] = f'S{s}'
           #slide['hidden'] = True
           #Add IDs to Components
           for c,component in enumerate(slide['props']['children']):
               component['id'] = f'S{s}_C{c}'

        #Convert from number to lists
        animation_l = []
        for slide in self.animation:
            tmp = []
            for x in slide:
             if not isinstance(x,list):
                #This is a number
                a = []
                for i in range(x):
                    a.append(0)
                a.append(1)
                tmp.append(a)
             else:    
               tmp.append(x)   
            animation_l.append(tmp)   
        #------------------------------        

        #Epans animations
        for x in animation_l:
            n_events = max([len(i) for i in x])
            for k,i in enumerate(x):
                #if len(i) < n_events:
                for i in  range(n_events - len(i)): 
                   x[k].append(1)
        #------------------------------- 
        #Add events
        events = {}
        for s,animation in enumerate(animation_l):
            animation = np.array(animation).T

            slide_events = []
            for i,click in enumerate(animation):
                event = {}
                for c,status in enumerate(click):
                    C_id = f'S{s}_C{c}'; value = not(bool(status))
                    event.update({C_id:value})
                slide_events.append(event)        
            events[f'S{s}'] = slide_events   


        return events    


   def show(self):
        """Display the presentation"""


        animation = self._render_animation()

        global data_to_serve
        data_to_serve = {'data':self.content,'animation':animation,'title':self.title}


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


   def save(self,filename):
        """Save presentation""" 

        animation = self._render_animation()

        content = {'data':self.content,'animation':animation}

        with open(filename,'w') as f: 
          json.dump(content,f)



   def push(self,**argv):

      #Prepare content
      animation = self._render_animation()
      content = {'data':self.content,'animation':animation,'title':self.title}

      url = push_data(content,**argv)




class Slide():
    """A simple example class"""
    def __init__(self,background='#303030',content = []):
        
         if len(content) == 0:
             self.content = {'type':'Slide','props':{'children':[],'className':'slide','style':{'backgroundColor':background}}}
         else:
          self.content = content  

         #Init animation
         self.animation = []
   
    def _add_animation(self,**argv):
        """Add animation"""

        animation = argv.setdefault('animation',[1])
        self.animation.append(animation)

    #componentA: eveything to show in presentation
    #componentA: eveything to show in grid

    def cite(self,key,**style):
        """Add a set of citation"""
        if not isinstance(key,list):
            keys = [key]
        else: keys = key    

        for i,key in enumerate(keys):
         text = Bibliography.format(key)
         style.update({'position':'absolute','left':'1%','bottom':f'{i*4+1}%'})
         style.setdefault('color','#FFFFFF')
         tmp = {'type':"Markdown",'props':{'children':text,'className':'markdownComponent interactable componentA','style':style.copy(),'fontsize':0.03}}
         self.content['props']['children'].append(tmp)
         self._add_animation(**style)

        return self
        

    def text(self,text,**argv):   
       
        #Adjust style---
        argv.setdefault('mode','center')
        style = get_style(**argv)
        style.setdefault('color','#FFFFFF')
        #-----------------
        nc = len(self.content['props']['children'])
        #tmp = {'type':"Markdown",'props':{'children':text,'className':'markdownComponent interactable','style':style},'id':f'C{nc}'}
        tmp = {'type':"Markdown",'props':{'children':text,'className':'markdownComponent interactable componentA','style':style,'fontsize':argv.setdefault('fontsize',0.04)}}
        self.content['props']['children'].append(tmp)
        self._add_animation(**argv)
        return self

    def model3D(self,filename,**argv):
        """Draw 3D model"""
        style = get_style(**argv)

        #Embedding
        #url = f"https://sketchfab.com/models/{filename}/embed?autostart=1&camera=0&ui_hint=0&dnt=1&transparent" 
        #tmp = {'type':'Iframe','props':{'className':'interactable componentA','src':url,'style':style}}
        
        #Local
        with open(filename, "rb") as f:
           model_data = base64.b64encode(f.read()).decode("utf8")
           url = 'data:model/gltf-binary;base64,{}'.format(model_data)


        tmp = {'type':'model3D','props':{'className':'interactable componentA','src':url,'style':style}}

        self.content['props']['children'].append(tmp)
        self._add_animation(**argv)
        return self



    def img(self,url,**argv):
        """Both local and URLs"""
        style = get_style(**argv)
        if argv.setdefault('frame',False):
            style['border'] = '2px solid red'

        if url[:4] != 'http':
            with open(url, "rb") as image_file:
               image =  base64.b64encode(image_file.read()).decode("utf8")
            url = 'data:image/png;base64,{}'.format(image)
        
        tmp = {'type':"Img",'props':{'src':url,'style':style,'className':'interactable componentA'}}
        self.content['props']['children'].append(tmp)
        self._add_animation(**argv)
        return self
     
    def slide(self,slide,**argv):
        """Nested slides"""

        #Adjust Slide
        style = get_style(**argv)
        style['backgroundColor'] = slide.content['props']['style']['backgroundColor']
        style['border'] = '3px solid #FFFFFF'
        tmp = {'type':'Slide','props':{'children':slide.content['props']['children'],'className':'embedded_slide interactable componentA','style':style}}
        #-----------------------------

        self.content['props']['children'].append(tmp)
        self._add_animation(**argv)
        return self
        

    def shape(self,shapeID,**argv):
       """add shape"""
       style = get_style(**argv)
       image = shape(shapeID,**argv)
       url = 'data:image/png;base64,{}'.format(image) 
       tmp = {'type':"Img",'props':{'src':url,'style':style,'className':'interactable componentA'}}
       self.content['props']['children'].append(tmp)
       self._add_animation(**argv)
       return self
       
    def youtube(self,videoID,**argv):
        """Add Youtube Video"""

        argv.setdefault('mode','full') 
        style = get_style(**argv)

        #Add Video--
        url = f"https://www.youtube.com/embed/{videoID}?controls=0&rel=0"
        #tmp = {'type':'Iframe','props':{'className':'PartA componentA','src':url,'style':style.copy()}}
        tmp = {'type':'Iframe','props':{'className':'interactable','src':url,'style':style.copy()}}
        self.content['props']['children'].append(tmp)
        #----------

        #Add thumbnail--
        #image = get_youtube_thumbnail(videoID)
        #url = 'data:image/png;base64,{}'.format(image)
        #style['visibility'] = 'hidden'
        #tmp = {'type':"Img",'props':{'src':url,'style':style,'className':'PartB interactable'}}
        #self.content['props']['children'].append(tmp)
        
        self._add_animation(**argv)
        return self

    def matplotlib(self,fig,**argv):
       """Add Matplotlib Image"""
       
       style = get_style(**argv)
       buf = io.BytesIO()
       fig.savefig(buf, format='png',bbox_inches="tight",transparent=True,pad_inches=0.5)
       buf.seek(0)
       image = base64.b64encode(buf.getvalue()).decode("utf8")
       buf.close()
       url = 'data:image/png;base64,{}'.format(image)
       tmp = {'type':"Img",'props':{'src':url,'style':style,'className':'interactable componentA'}}
       self.content['props']['children'].append(tmp)
       self._add_animation(**argv)

       return self


    def bokeh(self,graph,**argv):

       if isinstance(graph,str):
        with open(graph, 'r') as f:
          data = json.load(f)

      
       style  = get_style(**argv)
       tmp = {'type':"Bokeh",'graph':data,'props':{'style':style,'className':'componentA interactable'}}
       self.content['props']['children'].append(tmp)
       self._add_animation(**argv)
       return self 


    def plotly(self,graph,**argv):
       """Add plotly graph"""

       style  = get_style(**argv)
       if isinstance(graph,str):
         namefile = f'{graph}.json'
         fig = pio.read_json(namefile).to_plotly_json()
       else:  
          fig = graph.to_json()  
      
       #This clearly needs to be optimized
       #fig  = json_to_plotly(fig)
       #fig = process_plotly(fig)
       #fig = fig.to_plotly_json()
       #--------------------------
       
       #tmp = {'type':"Graph",'props':{'figure':{'layout':fig['layout'],'data':fig['data']},'style':style.copy(),'className':'PartA componentA interactable PLOTLY'}}
       tmp = {'type':"Plotly",'props':{'figure':{'layout':fig['layout'],'data':fig['data']},'style':style.copy(),'className':'componentA interactable PLOTLY'}}
       self.content['props']['children'].append(tmp)
       self._add_animation(**argv)
       return self 

    def molecule(self,structure,**argv):
       """Add Molecule"""

       argv.setdefault('mode','full') 
       style  = get_style(**argv) 
       tmp = {'type':'molecule','props':{'className':'interactable viewer_3Dmoljs componentA','style':style,'structure':structure,'backgroundColor':self.content['props']['style']['backgroundColor']}}

       self.content['props']['children'].append(tmp)
       self._add_animation(**argv)
       return self

    def REPL(self,kernel,**argv):
        style = get_style(**argv)

        kernel = argv.setdefault('kernel','python')
        code = argv.setdefault('code','')
        url = "https://jupyterlite.readthedocs.io/en/stable/_static/repl/index.html?kernel=python&theme=JupyterLab Dark&toolbar=1"

        #Add Iframe--
        tmp = {'type':'Iframe','props':{'className':'PartA componentA','src':url,'style':style,'hidden':False}}
        self.content['props']['children'].append(tmp)

        #Add Thumbnail
        image = load_icon('jupyter')
        image = encode_image_to_base64(image)
        url='data:image/png;base64,{}'.format(image)
        tmp = {'type':"Img",'props':{'src':url,'style':style,'className':'PartB','hidden':True}}
        self.content['props']['children'].append(tmp)

        self._add_animation(**argv)
        return self 
        
    def embed(self,url,**argv):

        #Add Iframe--
        style = get_style(**argv)
        #Add border
        #style['border'] ='2px solid #000';
        tmp = {'type':'Iframe','props':{'className':'interactable componentA','src':url,'style':style}}

        self.content['props']['children'].append(tmp)
        self._add_animation(**argv)
        return self


    def show(self):
        """Show the slide as a single-slide presentation"""
        
        Presentation([self]).show()


    def push(self,title='untitled'):
        """Show the slide as a single-slide presentation"""
        
        Presentation([self],title=title).push()



    #def add_app(self,func,func_options,**argv):
    #    self.apps.append([func,func_options,argv])

    

