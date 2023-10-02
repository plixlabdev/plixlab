import os
import requests
import base64
import io
import matplotlib.pyplot as plt
import json
import plotly.io as pio
from .utils import get_style,get_youtube_thumbnail,process_plotly,fig_to_base64,load_icon,encode_image_to_base64
from plotly.io import from_json as json_to_plotly
from .serve import run 
from .shape import run as shape



# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the style file
style_path = os.path.join(script_dir, 'assets', 'mpl_style')

# Use the style
plt.style.use(style_path)



        
class Presentation():
   """Class for presentations"""

   def __init__(self,slides,title='untitled'):


         self.title = title

         self.content = [slide.content for i,slide in enumerate(slides)]    

   @classmethod
   def read(cls,filename):
    """Import presentation"""   

    with open(filename,'r') as f:
       data = json.load(f)

       #prepare content
       slides = [Slide(content=content) for i,content in enumerate(data)]

       return cls(slides)

   
   def slide(self,**argv):  
         """Add a slide"""
          
         self.slides.append(Slide(**argv))

         return self.slides[-1]


   def show(self):
        """Display the presentation"""

        run(self.content)


   def save(self,filename):
      """Save presentation""" 

      content = [slide.content for slide in self.slides]
      with open(filename,'w') as f: 
          json.dump(content,f)



   def push(self,local=False,slide_index = 0,token=None):
   
      #Get token
      if not token: token = './computing_together.txt'
      with open(token,'r') as f:
           refresh_token = f.read()

      if local:
       url_prefix = 'http://127.0.0.1:5000/presentation'
       url ='http://127.0.0.1:5001/computo-306914/us-central1/uploadV2'
      else: 
       url_prefix = 'https://computo-306914.web.app/presentation'
       url = 'https://uploadv2-whn4gonsea-uc.a.run.app'


      # Get SignedURL--------------------------
      headers = {
      'Authorization': f'Bearer {refresh_token}',
      'Content-Type': 'application/json'
      }
      output = requests.post(url, json={"title": self.title}, headers=headers).json()
      signedURL = output['signedUrl']
      #----------------------------------------
    
     
      #Upload data
      content = [slide.content for slide in self.slides]
      response = requests.put(signedURL, headers={"Content-Type": "application/json"}, json=content)

      #Print URL
      print(url_prefix + '/' +  output['url'])



class Slide():
    """A simple example class"""
    def __init__(self,background='#36454f',content = []):
        
         if len(content) == 0:
          self.content = {'type':'Slide','props':{'children':[],'className':'slide presentation','style':{'backgroundColor':background}}}
         else:
          self.content = content  

   
    def text(self,text,**argv):   
       
        #Adjust style---
        argv.setdefault('mode','center')
        style = get_style(**argv)
        style.setdefault('color','#FFFFFF')
        style.update({'fontSize':argv.setdefault('fontsize',60)})
        #-----------------

        tmp = {'type':"Markdown",'props':{'children':text,'className':'markdownComponent interactable','style':style}}
        self.content['props']['children'].append(tmp)
        return self
    
    def img(self,url,**argv):
        """Both local and URLs"""
        style = get_style(**argv)

        if url[:4] != 'http':
            with open(url, "rb") as image_file:
               image =  base64.b64encode(image_file.read()).decode("utf8")
            url = 'data:image/png;base64,{}'.format(image)
        
        tmp = {'type':"Img",'props':{'src':url,'style':style,'className':'interactable'}}
        self.content['props']['children'].append(tmp)
        return self
     
    def slide(self,slide,**argv):
        """Nested slides"""

        #Adjust Slide
        style = get_style(**argv)
        style['backgroundColor'] = slide.content['props']['style']['backgroundColor']
        style['border'] = '3px solid #FFFFFF'
        tmp = {'type':'Slide','props':{'children':slide.content['props']['children'],'className':'embedded_slide interactable','style':style}}
        #-----------------------------

        self.content['props']['children'].append(tmp)
        return self
        

    def shape(self,shapeID,**argv):
       """add shape"""
       style = get_style(**argv)
       image = shape(shapeID,**argv)
       url = 'data:image/png;base64,{}'.format(image) 
       tmp = {'type':"Img",'props':{'src':url,'style':style,'className':'interactable'}}
       self.content['props']['children'].append(tmp)
       return self
       
    def youtube(self,videoID,**argv):
        """Add Youtube Video"""

        argv.setdefault('mode','full') 
        style = get_style(**argv)

        #Add Video--
        url = f"https://www.youtube.com/embed/{videoID}?controls=0&rel=0"
        tmp = {'type':'Iframe','props':{'className':'PartA','src':url,'style':style}}
        self.content['props']['children'].append(tmp)
        #----------

        #Add thumbnail--
        image = get_youtube_thumbnail(videoID)
        url = 'data:image/png;base64,{}'.format(image)
        tmp = {'type':"Img",'props':{'src':url,'style':style,'className':'PartB'}}
        self.content['props']['children'].append(tmp)
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
       tmp = {'type':"Img",'props':{'src':url,'style':style,'className':'interactable'}}
       self.content['props']['children'].append(tmp)

       return self

    def plotly(self,graph,**argv):
       """Add plotly graph"""

       style  = get_style(**argv)
       style['position'] = 'flex'

       if isinstance(graph,str):
         with open(f'{graph}.json','r') as f:
          fig = f.read()
       else:  
          fig = graph.to_json()  
      
       #This clearly needs to be optimized
       fig  = json_to_plotly(fig)
       fig = process_plotly(fig)
       fig = fig.to_plotly_json()
       #--------------------------
    
       tmp = {'type':"Graph",'props':{'figure':{'layout':fig['layout'],'data':fig['data']},'style':style,'className':'PartA'}}
       self.content['props']['children'].append(tmp)

       #Add thumbnail
       image = fig_to_base64(fig)
       url = 'data:image/png;base64,{}'.format(image)
       tmp = {'type':"Img",'props':{'src':url,'style':style,'className':'PartB','hidden':True}}
       self.content['props']['children'].append(tmp)

       return self 

    def molecule(self,structure,**argv):
       """Add Molecule"""

       argv.setdefault('mode','full') 
       style  = get_style(**argv) 
       tmp = {'type':'molecule','props':{'className':'interactable viewer_3Dmoljs','style':style,'structure':structure,'backgroundColor':self.content['props']['style']['backgroundColor']}}
       self.content['props']['children'].append(tmp)
    
       return self

    def REPL(self,kernel,**argv):
        style = get_style(**argv)

        kernel = argv.setdefault('kernel','python')
        code = argv.setdefault('code','')
        url = "https://jupyterlite.readthedocs.io/en/stable/_static/repl/index.html?kernel=python&theme=JupyterLab Dark&toolbar=1"

        #Add Iframe--
        tmp = {'type':'Iframe','props':{'className':'PartA','src':url,'style':style,'hidden':False}}
        self.content['props']['children'].append(tmp)

        #Add Thumbnail
        image = load_icon('jupyter')
        image = encode_image_to_base64(image)
        url='data:image/png;base64,{}'.format(image)
        tmp = {'type':"Img",'props':{'src':url,'style':style,'className':'PartB','hidden':True}}
        self.content['props']['children'].append(tmp)

        return self 
        
    def embed(self,url,**argv):

        #Add Iframe--
        style = get_style(**argv)
        #Add border
        style['border'] ='2px solid #000';
        tmp = {'type':'Iframe','props':{'className':'interactable','src':url,'style':style}}
        self.content['props']['children'].append(tmp)

        return self


    def show(self):
        """Show the slide as a single-slide presentation"""
        
        Presentation([self]).show()


    def push(self,title='untitled'):
        """Show the slide as a single-slide presentation"""
        
        Presentation([self],title=title).push()



    #def add_app(self,func,func_options,**argv):
    #    self.apps.append([func,func_options,argv])

    

