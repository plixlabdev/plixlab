import os
import time
import requests
import json
import base64
import io
import matplotlib.pyplot as plt
import plotly.io as pio
from .utils import get_style,get_youtube_thumbnail,process_plotly,fig_to_base64,load_icon,encode_image_to_base64
from plotly.io import from_json as json_to_plotly
#from .serve import run 
from .shape import run as shape
import os,sys
import json
import webbrowser
import numpy as np
from . import Bibliography
from urllib.parse import quote
import jsonpatch
from .server import run
import random
import string
from dict_hash import sha256



def update_values_for_key(d):

    token = 'src'

    print(d.keys())
    quit()

    def check(d):
      for key,value in d.items() :
        if key == token:

           d[key] = 'hello'
           print('here')
        else:  
            
            if isinstance(value,dict):
                print(key)
                check(d[key])

    check(d)

    quit()


# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the style file
style_path = os.path.join(script_dir, 'assets', 'mpl_style')
# Use the style
plt.style.use(style_path)


# List to store active WebSocket connections
#active_sockets = []




        #self.write_message(json.dumps(data_to_serve))


#class ReloadWebSocketHandler(websocket.WebSocketHandler):
#    def open(self):
#        active_sockets.append(self)
#
#    def on_close(self):
#        active_sockets.remove(self)


#data_to_serve = {}
#new = {}

         
#def get_access_token(local=False):


      #1. Look for a token in current directory
#      try : 
#       token = './plix_credentials.json'
#       with open(token,'r') as f:
#           cred = json.load(f)
#      except FileNotFoundError:
          #2. Look for a token from env
#          filename = os.path.expanduser("~") + '/.plix/plix_credentials.json'
#          try : 
#           with open(filename,'r') as f:
#            cred = json.load(f)
#          except FileNotFoundError:
             #3 subscribe
#             webbrowser.open_new_tab(url_subscribe)
#             quit()


#      return requests.post(f"https://securetoken.googleapis.com/v1/token?key={cred['apiKey']}",\
#                             {'grant_type':'refresh_token',\
#                             'refresh_token':cred['refreshToken']},\
#                             headers = { 'Content-Type': 'application/x-www-form-urlencoded' }).json()
      




def push_data(content,local=False,token=None,verbose=True):

      #Load credentials
      try : 
       with open(os.path.expanduser("~") + '/.plix/plix_credentials.json','r') as f:
            cred = json.load(f)
      except FileNotFoundError:
             webbrowser.open_new_tab(url_subscribe)
             quit()
   
      name = sha256({'title':content['title']})
      #get access token
      response = requests.post(f"https://securetoken.googleapis.com/v1/token?key={cred['apiKey']}",\
                             {'grant_type':'refresh_token',\
                             'refresh_token':cred['refreshToken']},\
                             headers = { 'Content-Type': 'application/x-www-form-urlencoded' }).json()

      accessToken = response['access_token']
      uid         = response['user_id']

       
      #Upload data
      url = f"https://firebasestorage.googleapis.com/v0/b/computo-306914.appspot.com/o?name=users/{uid}/tt55"
      response = requests.post(f"https://firebasestorage.googleapis.com/v0/b/computo-306914.appspot.com/o?name=users/{uid}/{name}",\
                                headers= {
                                        'Authorization': f'Bearer {accessToken}',
                                        "Content-Type": "application/json"
                                           },\
                                json = content).json()


      url = f"https://firebasestorage.googleapis.com/v0/b/computo-306914.appspot.com/o/users%2F{uid}/{name}"

      url = f'http://127.0.0.1:5000/presentation/?uid={uid}&name={name}'


      print(url)

  


      #Realtime Database, this will be fixed in the future---
      #url = f"http://localhost:9001/user/{uid}/test.json?ns=computo-306914"
      #response = requests.patch(url, headers=headers,json=content).json()
      #----

      #json_data = json.dumps(content)
      #key = hash(frozenset(content))
      #key = hash(json_data)
      #encoded_path = quote(f"{uid}/{key}", safe='')
      #Only live (use POST)
      #url = f"https://firebasestorage.googleapis.com/v0/b/computo-306914.appspot.com/o/users?name={uid}"

      #Production



#def push_data(content,local=False,token=None,verbose=True):


#      if local:
#       url_prefix = 'http://127.0.0.1:5000/presentation'
#       url ='http://127.0.0.1:5001/computo-306914/us-central1/upload'
#       url_subscribe = 'http://127.0.0.1:5000'
#      else: 
#       url_prefix = 'https://computo-306914.web.app/presentation'
#       url = 'https://upload-whn4gonsea-uc.a.run.app'


      #Get token
#      if not token: token = './computing_together.txt'

      #1. Look for a token in current directory
#      try : 
#       with open(token,'r') as f:
#           refresh_token = f.read()
#      except FileNotFoundError:
          #2. Look for a token from env
#          token = os.getenv('COMPUTING_TOGETHER_TOKEN',None)
#          try : 
#           with open(token,'r') as f:
#             refresh_token = f.read()
#          except FileNotFoundError:
             #3 subscribe
#             webbrowser.open_new_tab(url_subscribe)
#             quit()



      # Get SignedURL--------------------------
#      headers = {
#      'Authorization': f'Bearer {refresh_token}',
#      'Content-Type': 'application/json'
#      }
#      output = requests.post(url, json={"title": content['title']}, headers=headers).json()
#      signedURL = output['signedUrl']
      #----------------------------------------
    

      #Upload data

#      response = requests.put(signedURL, headers={"Content-Type": "application/json"}, json=content)

#      url = url_prefix + '/' +  output['url']
      #Print URL
#      if verbose:
#       print(url)

#      return url 




def generate_random_string(length):
    """Generate a random alphanumeric string of a given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

        
class Presentation():
   """Class for presentations"""

   def __init__(self,slides,title='default'):

            #assign a random title
            #title = 'title_' + generate_random_string(10) 

         self.title = title
         data = {}
         for slide in slides:
           data.update(slide.get())

         self.slides = data

         #self.animation = [slide.animation for slide in slides]

   


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

        run({'title':self.title,'slides':self.slides})

   

   def save(self,filename='output.json',library=True):
        """Save presentation""" 

        if library:
         filename = os.path.expanduser("~") + '/.plix/library.json'
      
         #Create if it does not exist
         if not os.path.isfile(filename):
          with open(filename,'w') as f: 
              json.dump({'presentations':{},'slides':{}},f)

         with open(filename,'r') as f: 
            data = json.load(f)
            if len(self.slides) > 1:
             data['presentations'][self.title] = list(self.slides.keys())
            data['slides'].update(self.slides)

         with open(filename,'w') as f: 
              json.dump(data,f)
            
        else:

         with open(filename,'w') as f: 
           json.dump(content,f)



   def push(self,**argv):

      #Prepare content
      content = {'title':self.title,'slides':self.slides}

      url = push_data(content,**argv)


class Collection:
    def __init__(self, slides):
        self.slides = slides

    def get(self):
        return self.slides


def Loader(name):

   filename = os.path.expanduser("~") + '/.plix/library.json'
   with open(filename,'r') as f: 
          data = json.load(f)

   #Check if the name is in presentations first
   if name in data['presentations'].keys():
      slides = {title:data['slides'][title] for title in data['presentations'][name]}
   elif name in data['slides'].keys():
       slides = {name:data['slides'][name]}
   else:
       print(f'No presentation or slide named {name}')
       quit()


   return Collection(slides)




class Slide():
    """A simple example class"""
    def __init__(self,title=None,background='#303030'):
        
         #if len(content) == 0:
         #self.content = {'children':{},'style':{'backgroundColor':background}}
         self.content = []
         self.style = {'backgroundColor':background}
         #else:
         #    self.content = content  



         #Init animation
         self.animation = []

         self.title = title
  

    def get(self):

        animation = self.process_animations()

        #Process title
        if not(self.title):
            self.title = sha256({'content':self.content,'style':self.style,'animation':animation})

        #Process children
        children = { self.title + '_' + str(k)  :tmp for k,tmp in enumerate(self.content)}

        data = {'children':children,'style':self.style,'animation':animation} 
            
        return {self.title:data}



    def _add_animation(self,**argv):
        """Add animation"""

        animation = argv.setdefault('animation',[1])
        self.animation.append(animation)

    def process_animations(self):

        #Convert from number to lists
        tmp = []
        for x in self.animation:
             if not isinstance(x,list):
                #This is a number
                a = []
                for i in range(x):
                    a.append(0)
                a.append(1)
                tmp.append(a)
             else:    
               tmp.append(x)   
        #------------------------------        

        #Expands animations
        tmp2 = [len(i) for i in tmp]
        if len(tmp2) > 0:
             n_events = max(tmp2)
             for k,i in enumerate(tmp):
                #if len(i) < n_events:
                for i in  range(n_events - len(i)): 
                   tmp[k].append(1)
        #------------------------------- 
        #Add events
        animation = np.array(tmp).T

        slide_events = []
        for i,click in enumerate(animation):
                event = {}
                for c,status in enumerate(click):
                    C_id = f'{c}'; value = not(bool(status))
                    event.update({C_id:value})
                slide_events.append(event)        

        return slide_events




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
         tmp = {'type':"Markdown",'text':text,'style':style.copy(),'fontsize':0.03}
         #self.children[f"{self.title}_{len(self.children)}"] = tmp
         self.content.append(tmp)
         self._add_animation(**style)

        return self
        

    def text(self,text,**argv):   
       
        #Adjust style---
        argv.setdefault('mode','center')
        style = get_style(**argv)
        style.setdefault('color','#FFFFFF')

        #-----------------
        tmp = {'type':"Markdown",'text':text,'fontsize':argv.setdefault('fontsize',0.04),'style':style}
        #self.content['children'].append(tmp)
        #self.children[f"{self.title}_{len(self.children)}"] = tmp
        self.content.append(tmp)
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


        tmp = {'type':'model3D','className':'interactable componentA','src':url,'style':style}

        self.content.append(tmp)

        self._add_animation(**argv)
        return self



    def img(self,url,**argv):
        """Both local and URLs"""
        if url[:4] != 'http':
            with open(url, "rb") as image_file:
               img = image_file.read()
               image =  base64.b64encode(img).decode("utf8")
            url = 'data:image/png;base64,{}'.format(image)
       
        style = get_style(**argv)
        if argv.setdefault('frame',False):
            style['border'] = '2px solid red'



        tmp = {'type':"Img",'src':url,'style':style}
        #self.content['children'].append(tmp)
        #self.content['children'][f"{self.title}_{len(self.content['children'])}"] = tmp
        #self.children[f"{self.title}_{len(self.children)}"] = tmp
        self.content.append(tmp)
        self._add_animation(**argv)
        return self
     
    #def slide(self,slide,**argv):
    #    """Nested slides"""

        #Adjust Slide
    #    style = get_style(**argv)
    #    style['backgroundColor'] = slide.content['props']['style']['backgroundColor']
    #    style['border'] = '3px solid #FFFFFF'
    #    tmp = {'type':'Slide','props':{'children':slide.content['props']['children'],'className':'embedded_slide interactable componentA','style':style}}
        #-----------------------------

   #     self.content['children'].append(tmp)
   #     self._add_animation(**argv)
   #     return self
        

    def shape(self,shapeID,**argv):
       """add shape"""
       style = get_style(**argv)
       image = shape(shapeID,**argv)
       url = 'data:image/png;base64,{}'.format(image) 
       tmp = {'type':"Img",'src':url,'style':style}
       #self.children[f"{self.title}_{len(self.children)}"] = tmp
       self.content.append(tmp)
       self._add_animation(**argv)
       return self
       
    def youtube(self,videoID,**argv):
        """Add Youtube Video"""

        argv.setdefault('mode','full') 
        style = get_style(**argv)

        #Add Video--
        url = f"https://www.youtube.com/embed/{videoID}?controls=0&rel=0"
        #tmp = {'type':'Iframe','props':{'className':'PartA componentA','src':url,'style':style.copy()}}
        tmp = {'type':'Iframe','className':'interactable','src':url,'style':style.copy()}
        #self.children[f"{self.title}_{len(self.children)}"] = tmp
        self.content.append(tmp)
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
       tmp = {'type':"Img",'src':url,'style':style}
       self.children[f"{self.title}_{len(self.children)}"] = tmp
       self._add_animation(**argv)

       return self


    def bokeh(self,graph,**argv):

       if isinstance(graph,str):
        with open(graph, 'r') as f:
          data = json.load(f)

      
       style  = get_style(**argv)
       tmp = {'type':"Bokeh",'graph':data,'style':style,'className':'componentA interactable'}
       self.content['children'].append(tmp)
       #self.children[f"{self.title}_{len(self.children)}"] = tmp
       self.content.append(tmp)
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
       
       tmp = {'type':"Plotly",'figure':{'layout':fig['layout'],'data':fig['data']},'style':style.copy()}
       #self.children[f"{self.title}_{len(self.children)}"] = tmp
       self.content.append(tmp)
       self._add_animation(**argv)
       return self 

    def molecule(self,structure,**argv):
       """Add Molecule"""

       argv.setdefault('mode','full') 
       style  = get_style(**argv) 
       tmp = {'type':'molecule','props':{'className':'interactable viewer_3Dmoljs componentA','style':style,'structure':structure,'backgroundColor':self.content['props']['style']['backgroundColor']}}

       self.content['children'].append(tmp)
       self._add_animation(**argv)
       return self

    def REPL(self,kernel,**argv):
        style = get_style(**argv)

        kernel = argv.setdefault('kernel','python')
        code = argv.setdefault('code','')
        url = "https://jupyterlite.readthedocs.io/en/stable/_static/repl/index.html?kernel=python&theme=JupyterLab Dark&toolbar=1"

        #Add Iframe--
        tmp = {'type':'Iframe','className':'PartA componentA','src':url,'style':style,'hidden':False}
        self.content['children'].append(tmp)

        #Add Thumbnail
        image = load_icon('jupyter')
        image = encode_image_to_base64(image)
        url='data:image/png;base64,{}'.format(image)
        tmp = {'type':"Img",'src':url,'style':style,'className':'PartB','hidden':True}
        self.content.append(tmp)
        #self.children[f"{self.title}_{len(self.children)}"] = tmp

        self._add_animation(**argv)
        return self 
        
    def embed(self,url,**argv):

        #Add Iframe--
        style = get_style(**argv)
        #Add border
        #style['border'] ='2px solid #000';
        tmp = {'type':'Iframe','src':url,'style':style}
        #self.children[f"{self.title}_{len(self.children)}"] = tmp
        self.content.append(tmp)

        self._add_animation(**argv)
        return self


    def show(self):
        """Show the slide as a single-slide presentation"""
        
        Presentation([self]).show()

    def save(self):
        """Save the slide"""
        
        Presentation([self]).save()


    def push(self,title='untitled'):
        """Show the slide as a single-slide presentation"""
        
        Presentation([self],title=title).push()



    #def add_app(self,func,func_options,**argv):
    #    self.apps.append([func,func_options,argv])

    

