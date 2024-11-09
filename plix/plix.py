import requests
import json
import base64
import io
import matplotlib.pyplot as plt
import plotly.io as pio
from .utils import get_style,process_plotly,process_bokeh
from .shape import run as shape
import os,sys
import json
import webbrowser
import numpy as np
from . import Bibliography
from urllib.parse import quote
from .server import run
import random
import string
from dict_hash import sha256
import msgpack
import pickle
import hashlib
from bokeh.embed import json_item
import random
import string


# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the style file
style_path = os.path.join(script_dir, 'assets', 'mpl_style')
# Use the style
plt.style.use(style_path)


def getsize(a):
    print('Size: ' + str(sys.getsizeof(a)/1024/1024) + ' Mb')


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

         self.presentation_ID = hashlib.md5(self.title.encode()).hexdigest()

         data = {}
         for slide in slides:
           data.update(slide.get(self.presentation_ID))

         self.slides = data

         #self.animation = [slide.animation for slide in slides]

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

   #def serialize_slides(self):

     #  for slide in self.slides.values():
     #      for component in slide['children'].values():
     #          if 'src' in component.keys():
     #              image =  base64.b64encode(component['src']).decode("utf8")
     #              url = 'data:image/png;base64,{}'.format(image)
     #              component['src'] = url
   

   def save(self,filename='output',library=False):
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

         content = {'title':self.title,'slides':self.slides}
      
         packed_data = msgpack.packb(content)

         # Save the serialized data to a file
        with open(filename + '.pkl', 'wb') as file:
          file.write(packed_data)

        return self    
   
   def share(self,local=False,token=None,verbose=True,visibility='public',emails = []):

      project_id = 'computo-306914'
      location   = 'us-central1'
      url_subscribe='https://computo.dev/signin'

      #Load credentials

      filename = os.path.expanduser("~") + '/.plix/plix_credentials.json'
      if not os.path.isfile(filename):
            webbrowser.open_new_tab(url_subscribe)
      else:      
            with open(filename,'r') as f:
                cred = json.load(f)
      # quit()
      #try : 
      # with open(os.path.expanduser("~") + '/.plix/plix_credentials.json','r') as f:
      #      cred = json.load(f)
      #except FileNotFoundError:
      #       webbrowser.open_new_tab(url_subscribe)
      #       quit()
   

      #get access token
      response = requests.post(f"https://securetoken.googleapis.com/v1/token?key={cred['apiKey']}",\
                             {'grant_type':'refresh_token',\
                             'refresh_token':cred['refreshToken']},\
                             headers = { 'Content-Type': 'application/x-www-form-urlencoded' }).json()

      accessToken = response['access_token']
      uid         = response['user_id']
   


      #Upload resources to cloud
      for slide in self.slides.values():
          for component_name,component in slide['children'].items():

              if 'src' in component.keys():
                  #print(component_name)
                  #METHOD 1: Signed URL
                  response = requests.post(f'https://{location}-{project_id}.cloudfunctions.net/generateSignedURL',\
                                 headers= {
                                        'Authorization': f'Bearer {accessToken}',
                                         "Content-Type": "application/json"},
                                         json ={'data':{'filename':f'users/{uid}/{component_name}'}}).json()
                  response = requests.put(response['result'],headers = {
                                         "Content-Type": "application/octet-stream"
                                         },
                                         data = component['src'])

                  component['src'] = f"https://firebasestorage.googleapis.com/v0/b/{project_id}.appspot.com/o?name=users/{uid}/{component_name}&alt=media"


      
      #Set order (because sometimes it gets messed up when uploaded)
      for k,slide in enumerate(self.slides.values()):
          slide['order'] = k
      #---------------------    
          
      presentation = {'title':self.title,'slides':self.slides}
      url =f"https://{project_id}-default-rtdb.firebaseio.com/users/{uid}/{self.presentation_ID}.json?auth={accessToken}&print=silent"
      response = requests.patch(url,json=presentation)
      #TODO: requests.patch inverts the slides' order

 
      #print(response)
      url = f'http://127.0.0.1:5000/share/?uid={uid}&name={self.presentation_ID}'
      print(url)

      url = f'https://{project_id}.web.app/share/?uid={uid}&name={self.presentation_ID}'
      print(url)

      url = f'https://computo.dev/share/?uid={uid}&name={self.presentation_ID}'
      print(url)

  
     




def generate_random_alphanumeric(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


class Slide():
    """A simple example class"""
    def __init__(self,title=None,background='#303030'):
        
       
         self.content = []
         self.style = {'backgroundColor':background}
       


         #Init animation
         self.animation = []

         if not title:
            title = generate_random_alphanumeric(10)  # Generate a 10-character long string
             
         #self.title = hashlib.md5(title.encode()).hexdigest()

         self.title = title
  

    def get(self,presentation_ID):

        animation = self.process_animations()

           
        slide_ID = presentation_ID + '_' + hashlib.md5(self.title.encode()).hexdigest()

        #Process children
        #children = {self.title + '_' + str(k)  :tmp for k,tmp in enumerate(self.content)}
        children = {slide_ID + '_' + str(k)  :tmp for k,tmp in enumerate(self.content)}

        data = {'children':children,'style':self.style,'animation':animation,'title':self.title} 
            

        return {slide_ID:data}



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


    def cite(self,key,**argv):
        """Add a set of citation"""
        if not isinstance(key,list):
            keys = [key]
        else: keys = key    

        for i,key in enumerate(keys):
         text = Bibliography.format(key)
         style.update({'position':'absolute','left':'1%','bottom':f'{i*4+1}%'})
         style.setdefault('color','#FFFFFF')

         tmp = {'type':"Markdown",'text':text,'style':style.copy(),'fontsize':argv.setdefault('fontsize',0.03)}
         self.content.append(tmp)
         self._add_animation(**style)

        return self
        

    def text(self,text,**argv):   
       
        #Adjust style---
        argv.setdefault('mode','center')
        style = get_style(**argv)
        style.setdefault('color','#DCDCDC')

        #-----------------
        tmp = {'type':"Markdown",'text':text,'fontsize':argv.setdefault('fontsize',0.1),'style':style}
       
        self.content.append(tmp)
        self._add_animation(**argv)
        return self

    def model3D(self,filename,**argv):
        """Draw 3D model"""
        style = get_style(**argv)

        
        #Local
        with open(filename, "rb") as f:
        
           url = f.read()

        tmp = {'type':'model3D','className':'interactable componentA','src':url,'style':style}

        self.content.append(tmp)

        self._add_animation(**argv)
        return self



    def img(self,url,**argv):
        """Both local and URLs"""

        if url[:4] != 'http':
            with open(url, "rb") as f:             
               url  = f.read()
      
        #/Add border
        style = get_style(**argv)
        if argv.setdefault('frame',False):
            style['border'] = '2px solid ' + argv.setdefault('frame_color','#DCDCDC')


        tmp = {'type':"Img",'src':url,'style':style}
        self.content.append(tmp)
        self._add_animation(**argv)
        return self
     
   
        

    def shape(self,shapeID,**argv):
       """add shape"""
       style = get_style(**argv)
       image = shape(shapeID,**argv)
       #url = 'data:image/png;base64,{}'.format(image) 
       tmp = {'type':"Img",'src':image,'style':style}
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
        tmp = {'type':'Iframe','className':'interactable','src':url,'style':style.copy()}
        self.content.append(tmp)
        #----------

     
        self._add_animation(**argv)
        return self

    def matplotlib(self,fig,**argv):
       """Add Matplotlib Image"""
       
       style = get_style(**argv)
       buf = io.BytesIO()
       fig.savefig(buf, format='png',bbox_inches="tight",transparent=True)
       buf.seek(0)
       url = buf.getvalue()
       buf.close()
       tmp = {'type':"Img",'src':url,'style':style}

       self.content.append(tmp)
       self._add_animation(**argv)

       return self


    def bokeh(self,graph,**argv):

   

       process_bokeh(graph)
       style  = get_style(**argv)
       item = json_item(graph)

       tmp = {'type':"Bokeh",'graph':item,'style':style}
       self.content.append(tmp)
       self._add_animation(**argv)
       return self


    def plotly(self,fig,**argv):
       """Add plotly graph"""

       style  = get_style(**argv)
   
       fig = process_plotly(fig)
     
       fig = fig.to_json()
       #--------------------------
     
       tmp = {'type':"Plotly",'figure':fig,'style':style.copy()}
      
       self.content.append(tmp)
       self._add_animation(**argv)
       return self 

    def molecule(self,structure,**argv):
       """Add Molecule"""
       
       argv.setdefault('mode','full') 
       style  = get_style(**argv) 

       tmp = {'type':'molecule','style':style,'structure':structure,'backgroundColor':self.style['backgroundColor']}

       self.content.append(tmp)
       self._add_animation(**argv)
       return self 


    def python(self,**argv):
        style = get_style(**argv)

        kernel = argv.setdefault('kernel','python')
        code = argv.setdefault('code','')
        url = "https://jupyterlite.readthedocs.io/en/stable/_static/repl/index.html?kernel=python&theme=JupyterLab Dark&toolbar=1"


        tmp = {'type':'Iframe','url':url,'style':style}
        self.content.append(tmp)
        self._add_animation(**argv)

     
        return self 
        
    def embed(self,url,**argv):

        #Add Iframe--
        style = get_style(**argv)
        #Add border
        #style['border'] ='2px solid #000';
        tmp = {'type':'Iframe','url':url,'style':style}
        self.content.append(tmp)
        self._add_animation(**argv)
        return self


    def show(self):
        """Show the slide as a single-slide presentation"""
        
        Presentation([self]).show()

    def save(self,*args,**kwargs):
        """Save the slide"""
        
        Presentation([self]).save(*args,**kwargs)

        return self


    def share(self,title='untitled'):
        """Show the slide as a single-slide presentation"""
        
        Presentation([self],title=title).share()

