import sys
import json
from plix import Presentation

def init():
  """Read file"""

  filename =  sys.argv[1]

  with open(filename,'r') as f:
       data = json.load(f)

  Presentation.read(data).show()

