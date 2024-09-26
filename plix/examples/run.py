from plix import Slide,Presentation,Bibliography
import plotly.express as px


prefix = '../../docs/source/_static/examples/'

#s1 = Slide().text('Welcome to PLIX!').img('assets/logo.png',y=0.1,w=0.2)
#
#df = px.data.iris()

#fig = px.scatter(df, x="sepal_width", \
#                     y="sepal_length", \
#                     color="species")

#s2 = Slide().plotly(fig)

#Presentation([s1,s2]).save(prefix + 'presentation')


#Markdown
#Slide().text('<u> This </u> **text** is *really important*.',x=0.1,y=0.6,fontsize=0.1,color='orange').save(prefix + 'markdown').show()

#Image
#Slide().img('assets/image.png',x=0.2,y=0.3,w=0.65).show()

#quit()


def markdown():
    
 from plix import Slide

 Slide().text('<u> This </u> **text** is *really important*.',x=0.2,y=0.6,\
               fontsize=0.1,color='orange').show()

def plotly_example():

 from plix import Slide
 import plotly.express as px

 df = px.data.iris()

 fig = px.scatter(df, x="sepal_width", \
                      y="sepal_length", \
                      color="species")

 Slide().plotly(fig).save(prefix + 'plotly').show()



def run_matplotlib():

 #Matplotlib
 import numpy as np
 import matplotlib.pyplot as plt
 from plix import Slide

 # Create data points
 x = np.linspace(0, 2 * np.pi, 100)
 y = np.sin(x)

 # Plot the sine wave
 fig = plt.figure(figsize=(8, 4.5))
 plt.plot(x, y, label='Sine Wave')
 plt.title('Simple Sine Wave')
 plt.xlabel('x values')
 plt.ylabel('y values')

 Slide().matplotlib(fig).save(prefix + 'matplotlib')

def run_shape():

        Slide().shape('arrow',x=0.2,y=0.45,w=0.2,orientation=45,color=[1,0.015,0]).\
                shape('square',x=0.6,y=0.5,w=0.2,aspect_ratio=0.25).save(prefix + 'shape').show()

def run_web():

    url = 'https://examples.pyscriptapps.com/antigravity/latest/'
    Slide().embed(url).save(prefix + 'embed')


#run_web()
def run_youtube():

 from plix import Slide 

 Slide().youtube('zDtx6Z9g4xA').save(prefix + 'youtube').show()

#run_youtube()    

#plotly_example() 


def example_bokeh() :

 from plix import Slide
 from bokeh.plotting import figure, show

 x = [1, 2, 3, 4, 5]
 y = [6, 7, 2, 4, 5]


 p = figure(
    x_axis_label='x',
    y_axis_label='y'
 )

 p.line(x, y, legend_label="Temp.", line_width=2)

 Slide().bokeh(p).save(prefix + 'bokeh').show()




def example_molecule() :

 from plix import Slide 

 Slide().molecule('7R5N').save(prefix + 'molecule')

#example_molecule()

def example_REPL():

  Slide().REPL('python').save(prefix + 'REPL')

#example_REPL()

def example_model3d():

    #Slide().model3D('assets/model.glb').save(prefix + 'model').show()
    Slide().model3D('assets/Blue_end.glb').text('Blue Flower Animated" (https://skfb.ly/oDIqT) by morphy.vision is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).',y=0.1,fontsize=0.03).save(prefix + 'flower').show()

#def example_model3d_dragon():

    #Slide().model3D('assets/dragon_gold.glb').save(prefix + 'model_dragon').show()

##example_model3d_dragon()
#quit()


def example_citations():

    Slide().text(Bibliography.format('einstein1935'),fontsize=0.05,x=0.3,y=0.6).save(prefix + 'citation_text').show()
    #Slide().cite('einstein1935').save(prefix + 'citation').show()

#example_citations()
    
def animation():

   Slide().text('Text #1',y=0.7).\
           text('Text #2',y=0.5,animation=1).\
           text('Text #3',y=0.3,animation=2).save(prefix + 'animation').show()
   

#animation()    

def animation2():

   Slide().text('Text #1',y=0.7).\
           text('Text #2',y=0.5,animation=[1,0,1]).\
           text('Text #3',y=0.3,animation=2).save(prefix + 'animation').show()
   

#animation2()    



#example_model3d()
markdown()

#example_bokeh()

#save(prefix + 'welcome')

#Slide().img('assets/image.png').text('''<a href='https://pngtree.com/freepng/music-note-staves_8445985.html'>png image from pngtree.com/</a>''',y=0.1,fontsize=0.03).show()
#Slide().img('assets/image.png').save(prefix + 'example_2')

#Slide().img('assets/image.png',w=0.4,x=0.2,y=0.4,animation=0).\
#          text('Hello, World!',x=0.7,y=0.5,fontsize=0.05,animation=1).save(prefix + 'example_4')

 
#S1 = Slide().text('Slide 1')
#S2 = Slide().text('Slide 2')




#Slide().plotly(fig).save(prefix + 'plotly_example')

