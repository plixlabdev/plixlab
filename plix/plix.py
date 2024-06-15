import time
import requests
import json
import base64
import io
import matplotlib.pyplot as plt
import plotly.io as pio
from .utils import get_style,get_youtube_thumbnail,process_plotly,fig_to_base64,load_icon,encode_image_to_base64,process_bokeh
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
import msgpack
import pickle
import hashlib
from .remote_server import run_watchdog
from bokeh.embed import json_item



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
      


def getsize(a):
    print('Size: ' + str(sys.getsizeof(a)/1024/1024) + ' Mb')






#def push_data_old(content,local=False,token=None,verbose=True):

      #Load credentials
#      try : 
#       with open(os.path.expanduser("~") + '/.plix/plix_credentials.json','r') as f:
#            cred = json.load(f)
#      except FileNotFoundError:
#             webbrowser.open_new_tab(url_subscribe)
#             quit()
   

#      name = hashlib.md5(content['title'].encode()).hexdigest()


      #get access token
#      response = requests.post(f"https://securetoken.googleapis.com/v1/token?key={cred['apiKey']}",\
#                             {'grant_type':'refresh_token',\
#                             'refresh_token':cred['refreshToken']},\
#                             headers = { 'Content-Type': 'application/x-www-form-urlencoded' }).json()

#      accessToken = response['access_token']
#      uid         = response['user_id']


    
      #Update visibility---
      #This can work only when cross-service between firestore and realtime database
      #url = 'https://firestore.googleapis.com/v1/projects/computo-306914/databases/(default)/documents/users/admin'

      # The new data to add
      #data = {
      #  'fields': {
      #  'age': {
      #      'integerValue': '30'  # Adding a new field 'age' with value 30
      #    }
      #   }}

      #response = requests.patch(url,\
      #                          headers= {
      #                                   "Content-Type": "application/json"
      #                                     },\
      #                                    data = json.dumps(data))
      #print(response.text)

      #---------------------

      #quit()


      #Upload data to Cloud Storage (Production)
      #response = requests.post(f"https://firebasestorage.googleapis.com/v0/b/computo-306914.appspot.com/o?name=users/{uid}/{name}",\
      #                          headers= {
      #                                  'Authorization': f'Bearer {accessToken}',
      #                                   "Content-Type": "application/octet-stream"
      #                                     },\
      #                          data = msgpack.packb(content,use_bin_type=True))
      #------------------------------------------

      #Local database
      #url = f"http://localhost:9001/test.json/?ns=computo-306914"
      #response = requests.put(url,\
      #                          headers= {
      #                                   "Content-Type": "application/json"
      #                                     },\
      #                          json=content)
      #print(response)
      #----------------------------

      #
      #Upload to Cloud Storage (Local) [This does not work, it gives 501]
      #url = f"http://localhost:9199/o?name=users/{uid}/{name}&ns=computo-306914"
      #response = requests.post(url,\
      #                          headers= {
      #                                  'Authorization': f'Bearer {accessToken}',
      #                                   "Content-Type": "application/octet-stream"
      #                                     },\
      #                          data = msgpack.packb(content,use_bin_type=True))
      #print(response)
      #----------------------------


      #add visibility
      #data = {'content':content,'visibility':['giusepperomano82@gmail.com']}

      #Upload resources to cloud
 #     for slide in content['slides'].values():
 #         for component_name,component in slide['children'].items():

  #            if 'src' in component.keys():
                  #METHOD 1: Signed URL
  #                response = requests.post('https://us-central1-computo-306914.cloudfunctions.net/generateSignedURL',\
  #                               headers= {
  #                                      'Authorization': f'Bearer {accessToken}',
  #                                       "Content-Type": "application/json"},
  #                                       json ={'data':{'filename':f'users/{uid}/{component_name}'}}).json()
                  #print(response)

                  #getsize(component['src'])
                  
                  #print(response['result'])
   #               response = requests.put(response['result'],headers = {
   #                                      "Content-Type": "application/octet-stream"
   #                                      },
   #                                      data = component['src'])

                  #print(response)             
                  #resource_url =     f"https://firebasestorage.googleapis.com/v0/b/computo-306914.appspot.com/o?name=users/{uid}/{component_name}"

    #              component['src'] = f"https://firebasestorage.googleapis.com/v0/b/computo-306914.appspot.com/o?name=users/{uid}/{component_name}&alt=media"
                  #print(response)                       

                  
                  #METHOD 2:Upload resource to Storage and retrieve URL (this will provide the download token
                 #response = requests.post(f"https://firebasestorage.googleapis.com/v0/b/computo-306914.appspot.com/o?name=users/{uid}/{name}",\
                 #               headers= {
                 #                       'Authorization': f'Bearer {accessToken}',
                 #                        "Content-Type": "application/octet-stream"
                 #                          },\
                         #               data = component['src'])
                 #print(response.json())


      #Upload to Real Time Databse (Local)
      #response = requests.put(f"http://localhost:9001/test.json/?ns=computo-306914",\
      #                          headers= {
      #                                   "Content-Type": "application/json"
      #                                     },\
      #                          json=content)
      #print(response.json())
      #----------------------------

      #Upload to Real Time Databse (production)
      #url = f"http://localhost:9001/test.json/?ns=computo-306914"

     # content_2 = content.copy()
      #content_2['title'] = 'st'
      #ori = {}

      #Update only changes
     # patch = list(jsonpatch.JsonPatch.from_diff({},content))
      #print(patch)


     # old_data = {}
     # if os.path.isfile('./.cache') :
     #       with open('./.cache','r') as f:
     #           old_data = json.load(f)
#
     # patch = list(jsonpatch.JsonPatch.from_diff(old_data,content))

     # if len(patch) > 0:

            #self.write_message(json.dumps({'patch':patch}))
     #   with open('./.cache','w') as f:
     #       json.dump(content,f)


      #db = 'computo-306914-default-rtdb'

      #for p in patch:
      #    if p['op'] == 'remove':
      #      if local:
      #        url= f'http://localhost:9001/users/{uid}/{name}.json/?ns=computo-306914' 
      #      else:  
      #        url= f'https://{db}.firebaseio.com/users/{uid}/{name}.json?auth={accessToken}'
      #      response = requests.delete(url,json=p['path'])

      #    if p['op'] in ['add','replace']:
      #        if local:  
      #         url = f"http://localhost:9001/users/{uid}/{name}{p['path']}.json/?ns=computo-306914&print=silent"
      #        else: 
      #         url =f"https://{db}.firebaseio.com/users/{uid}/{name}{p['path']}.json?auth={accessToken}&print=silent"

      #        response = requests.put(url,json=p['value'])
              #print(response)


      #Update the whole document
      #local
      #response = requests.put(f'http://localhost:9001/users/{uid}/{name}.json/?ns=computo-306914',json=content)
      #global
      ##response = requests.put(f'https://computo-306914.firebaseio.com/users/{uid}/{name}.json?auth={accessToken}',json=content)
      #print(response)
      #print(response.json())
      #----------------------------

      #Update visibility
      

 
      #if local:
      #url = f'http://127.0.0.1:5000/presentation/?uid={uid}&name={name}'
      #print(url)

      #else :
      #url = f'https://computo-306914.web.app/presentation/?uid={uid}&name={name}'
      #print(url)

      #https://computo-306914.web.app/presentation


  



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

         self.presentation_ID = hashlib.md5(self.title.encode()).hexdigest()

         data = {}
         for slide in slides:
           data.update(slide.get(self.presentation_ID))

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

   #def write_html(self):
   #    """Write HTML"""


   def show(self):
        """Display the presentation"""

        run({'title':self.title,'slides':self.slides})

   def serialize_slides(self):

       for slide in self.slides.values():
           for component in slide['children'].values():
               if 'src' in component.keys():
                   image =  base64.b64encode(component['src']).decode("utf8")
                   url = 'data:image/png;base64,{}'.format(image)
                   component['src'] = url
   

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

         #self.serialize_slides() #This changes bytes to base64 in order to make it serializable

         content = {'title':self.title,'slides':self.slides}
         #with open(filename + '.json','w') as f: 
         #  json.dump({'title':self.title,'slides':self.slides},f)
         #with open(filename + '.pkl','wb') as f: 
         #  pickle.dump({'title':self.title,'slides':self.slides},f)

         packed_data = msgpack.packb(content)

         # Save the serialized data to a file
        with open(filename + '.pkl', 'wb') as file:
          file.write(packed_data)



        return self    



   def share(self,local=False,token=None,verbose=True,visibility='public',emails = []):

      project_id = 'computo-306914'
      location   = 'us-central1'

      #Load credentials
      try : 
       with open(os.path.expanduser("~") + '/.plix/plix_credentials.json','r') as f:
            cred = json.load(f)
      except FileNotFoundError:
             webbrowser.open_new_tab(url_subscribe)
             quit()
   
      #name = hashlib.md5(content['title'].encode()).hexdigest()

      #get access token
      response = requests.post(f"https://securetoken.googleapis.com/v1/token?key={cred['apiKey']}",\
                             {'grant_type':'refresh_token',\
                             'refresh_token':cred['refreshToken']},\
                             headers = { 'Content-Type': 'application/x-www-form-urlencoded' }).json()

      accessToken = response['access_token']
      uid         = response['user_id']
      email       = cred['email']
      #-----------------------------------

      #Add visibility
      print(visibility)
      if visibility == 'public':
         recipients = ['public']
      elif visibility == 'private':    
         recipents = [email]
      elif visibility == 'custom':    
         recipients = emails
      else:   
         print('No visibility recognized') 
         quit()

      visibility = {r.replace('.',','):True for r in recipients}

      #Upload resources to cloud
      for slide in self.slides.values():
          for component_name,component in slide['children'].items():

              if 'src' in component.keys():
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

      visibility = {r.replace('.',','):True for r in recipients}

      #Upload slides--
      url =f"https://{project_id}-default-rtdb.firebaseio.com/users/{uid}/slides.json?auth={accessToken}&print=silent"

      #Add visibility to slides
      for key,value in self.slides.items():
          value['visibility'] = visibility

      

      response = requests.patch(url,json=self.slides)
      print(response)

      #Upload presentations--
      url =f"https://{project_id}-default-rtdb.firebaseio.com/users/{uid}/presentations/{self.presentation_ID}.json?auth={accessToken}&print=silent"
      presentations = {'title':self.title,'slide_IDs':{key:value['title'] for key,value in self.slides.items()},'visibility':visibility}
      response = requests.patch(url,json=presentations)

      print(response)
     
      #print(response)
      url = f'http://127.0.0.1:5000/presentation/?uid={uid}&name={self.presentation_ID}'
      print(url)

      url = f'https://{project_id}.web.app/presentation/?uid={uid}&name={self.presentation_ID}'
      print(url)

   def push_old(self,local=False,token=None,verbose=True,visibility='public',emails = []):

      project_id = 'computo-306914'
      location   = 'us-central1'

      #Load credentials
      try : 
       with open(os.path.expanduser("~") + '/.plix/plix_credentials.json','r') as f:
            cred = json.load(f)
      except FileNotFoundError:
             webbrowser.open_new_tab(url_subscribe)
             quit()
   
      #name = hashlib.md5(content['title'].encode()).hexdigest()

      #get access token
      response = requests.post(f"https://securetoken.googleapis.com/v1/token?key={cred['apiKey']}",\
                             {'grant_type':'refresh_token',\
                             'refresh_token':cred['refreshToken']},\
                             headers = { 'Content-Type': 'application/x-www-form-urlencoded' }).json()

      accessToken = response['access_token']
      uid         = response['user_id']
      email       = cred['email']
      #print(accessToken)
      #-----------------------------------

      #Add visibility
      print(visibility)
      if visibility == 'public':
         recipients = ['public']
      elif visibility == 'private':    
         recipents = [email]
      elif visibility == 'custom':    
         recipients = emails
      else:   
         print('No visibility recognized') 
         quit()

      data = {'title':self.title,'slides':self.slides,'visibility':{r.replace('.',','):True for r in recipients}}

      #Upload resources to cloud
      for slide in data['slides'].values():
          for component_name,component in slide['children'].items():

              if 'src' in component.keys():
                  #METHOD 1: Signed URL
                  response = requests.post(f'https://{location}-{project_id}.cloudfunctions.net/generateSignedURL',\
                                 headers= {
                                        'Authorization': f'Bearer {accessToken}',
                                         "Content-Type": "application/json"},
                                         json ={'data':{'filename':f'users/{uid}/{component_name}'}}).json()
                  #print(response)

                  #getsize(component['src'])
                  
                  #print(response['result'])
                  response = requests.put(response['result'],headers = {
                                         "Content-Type": "application/octet-stream"
                                         },
                                         data = component['src'])

                  component['src'] = f"https://firebasestorage.googleapis.com/v0/b/{project_id}.appspot.com/o?name=users/{uid}/{component_name}&alt=media"
                  #print(response)                       


      #Create patches
      content_2 = data.copy()
      #Update only changes
      patch = list(jsonpatch.JsonPatch.from_diff({},data))


      old_data = {}
      if os.path.isfile('./.cache') :
            with open('./.cache','r') as f:
                old_data = json.load(f)

      patch = list(jsonpatch.JsonPatch.from_diff(old_data,data))

      #if len(patch) > 0:
      #  with open('./.cache','w') as f:
      #      json.dump(content,f)

      #Update patches to database
      for p in patch:
          if p['op'] == 'remove':
            if local:
              url= f'http://localhost:9001/users/{uid}/presentations/{name}.json/?ns={project_id}' 
            else:  
              url= f'https://{project_id}-default-rtdb.firebaseio.com/users/{uid}/presentations/{self.presentation_ID}.json?auth={accessToken}'
            response = requests.delete(url,json=p['path'])

          if p['op'] in ['add','replace']:
              if local:  
               url = f"http://localhost:9001/users/{uid}/presentations/{name}{p['path']}.json/?ns={project_id}&print=silent"
              else: 
               url =f"https://{project_id}-default-rtdb.firebaseio.com/users/{uid}/presentations/{self.presentation_ID}{p['path']}.json?auth={accessToken}&print=silent"
              response = requests.put(url,json=p['value'])
              #if not response.status_code == '204':
              print(response)
                  #quit()

      url = f'http://127.0.0.1:5000/presentation/?uid={uid}&name={self.presentation_ID}'
      print(url)

      url = f'https://{project_id}.web.app/presentation/?uid={uid}&name={self.presentation_ID}'
      print(url)
      #Prepare content
      #content = {'title':self.title,'slides':self.slides}
      

      #print('pushing data')
      #url = push_data(content,self.presentation_ID,**argv)
     
      if os.environ.get('RUNNING_FROM_WATCHDOG'):
         print('already running')
      else:   
         print('start watchdog')
         run_watchdog()

   #def push(self,**argv):

      #Prepare content
   #   content = {'title':self.title,'slides':self.slides}
      

   #   print('pushing data')
   #   url = push_data(content,self.presentation_ID,**argv)
     
   #   if os.environ.get('RUNNING_FROM_WATCHDOG'):
   #      print('already running')
   #   else:   
   #      print('start watchdog')
   #      run_watchdog()
      


class Collection:
    def __init__(self, slides):
        self.slides = slides

    def get(self):
        return self.slides


def Loader(name):

   filename = os.path.expanduser("~") + '/.plix/library.json'
   with open(filename,'r') as f: 
          data = json.load(f)

   quit()
   #Check if the name is in presentations first
   if name in data['presentations'].keys():
      slides = {title:data['slides'][title] for title in data['presentations'][name]}
   elif name in data['slides'].keys():
       slides = {name:data['slides'][name]}
   else:
       print(f'No presentation or slide named {name}')
       quit()


   return Collection(slides)


import random
import string

def generate_random_alphanumeric(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# Example usage




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



    #componentA: eveything to show in presentation
    #componentA: eveything to show in grid

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
        style.setdefault('color','#FFFFFF')

        #-----------------
        tmp = {'type':"Markdown",'text':text,'fontsize':argv.setdefault('fontsize',0.1),'style':style}
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
           #model_data = base64.b64encode(f.read()).decode("utf8")
           #url = 'data:model/gltf-binary;base64,{}'.format(model_data)
           url = f.read()

        tmp = {'type':'model3D','className':'interactable componentA','src':url,'style':style}

        self.content.append(tmp)

        self._add_animation(**argv)
        return self



    def img(self,url,**argv):
        """Both local and URLs"""

        if url[:4] != 'http':
            with open(url, "rb") as f:
               #img = f.read()
               #image =  base64.b64encode(img).decode("utf8")
               #url = 'data:image/png;base64,{}'.format(image)

               url  = f.read()
      
        #/Add border
        style = get_style(**argv)
        if argv.setdefault('frame',False):
            style['border'] = '2px solid red'


        tmp = {'type':"Img",'src':url,'style':style}
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
       fig.savefig(buf, format='png',bbox_inches="tight",transparent=True)
       buf.seek(0)
       #image = base64.b64encode(buf.getvalue()).decode("utf8")
       #buf.close()
       #url = 'data:image/png;base64,{}'.format(image)
       url = buf.getvalue()
       buf.close()
       tmp = {'type':"Img",'src':url,'style':style}

       self.content.append(tmp)
       self._add_animation(**argv)

       return self


    def bokeh(self,graph,**argv):

       #if isinstance(graph,str):
       # with open(graph, 'r') as f:
       #   data = json.load(f)

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
       #if isinstance(graph,str):
       #  namefile = f'{graph}.json'
       #  fig = pio.read_json(namefile).to_plotly_json()
       #else:  
       # fig = graph.to_json()  
      
       #This clearly needs to be optimized
       #fig  = json_to_plotly(fig)
       fig = process_plotly(fig)
       #fig = fig.to_plotly_json()
       fig = fig.to_json()
       #--------------------------
      
       #tmp = {'type':"Plotly",'figure':{'layout':fig['layout'],'data':fig['data']},'style':style.copy()}
       tmp = {'type':"Plotly",'figure':fig,'style':style.copy()}
       #self.children[f"{self.title}_{len(self.children)}"] = tmp
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


    def python(self,kernel,**argv):
        style = get_style(**argv)

        kernel = argv.setdefault('kernel','python')
        code = argv.setdefault('code','')
        url = "https://jupyterlite.readthedocs.io/en/stable/_static/repl/index.html?kernel=python&theme=JupyterLab Dark&toolbar=1"


        tmp = {'type':'Iframe','src':url,'style':style}
        self.content.append(tmp)
        self._add_animation(**argv)

        #Add Iframe--
        #tmp = {'type':'Iframe','className':'PartA componentA','src':url,'style':style,'hidden':False}
        #tmp = {'type':'Iframe','src':url,'style':style}
        #self.content['children'].append(tmp)

        #Add Thumbnail
        #image = load_icon('jupyter')
        #image = encode_image_to_base64(image)
        #url='data:image/png;base64,{}'.format(image)
        #tmp = {'type':"Img",'src':url,'style':style,'className':'PartB','hidden':True}
        #self.content.append(tmp)

        #self._add_animation(**argv)
        return self 
        
    def embed(self,url,**argv):

        #Add Iframe--
        style = get_style(**argv)
        #Add border
        #style['border'] ='2px solid #000';
        tmp = {'type':'Iframe','src':url,'style':style}
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



    #def add_app(self,func,func_options,**argv):
    #    self.apps.append([func,func_options,argv])

    

