import sys
import json
from plix import Presentation

def init():
  """Read file"""

  filename =  sys.argv[1]

  Presentation.read(filename).show()

