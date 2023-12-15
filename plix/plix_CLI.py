import sys,os
import json
#from plix import Presentation
from .server import run

def init():
  """Read file"""

  #Action
  action =  sys.argv[1]

  if action == 'show':

   presentation = sys.argv[2]    

   filename = os.path.expanduser("~") + '/.plix/library.json'
   with open(filename,'r') as f: 
          data = json.load(f)

   slide_titles = data['presentations'][presentation]

   slides = {title:data['slides'][title] for title in slide_titles}

   run({'title':presentation,'slides':slides})

  elif action == 'delete':
   name = sys.argv[2]    
   filename = os.path.expanduser("~") + '/.plix/library.json'
   if os.path.isfile(filename):
    with open(filename,'r') as f: 
        data = json.load(f)

    if name in data['presentations'].keys(): del data['presentations'][name]    
    if name in data['slides'].keys(): del data['slides'][name]    

    with open(filename,'w') as f: 
        json.dump(data,f)


   
  elif action == 'list':

     filename = os.path.expanduser("~") + '/.plix/library.json'
     with open(filename,'r') as f: 
          data = json.load(f)

     print(' ')    
     print('\033[94m' + 'Slides' + '\033[0m')
     for i in data['slides'].keys():
         print(i)
     print(' ')    

     print('\033[94m' + 'Presentations' + '\033[0m')
     for i in data['presentations'].keys():
         print(i)
     print(' ')    


  elif action == 'init':
    filename = os.path.expanduser("~") + '/.plix/library.json'
    with open(filename,'w') as f:
              json.dump({'presentations':{},'slides':{}},f)



