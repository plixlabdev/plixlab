import cairo
import base64
from io import BytesIO
from .utils import hex_to_rgb
import numpy as np
 
 

def arrow(context, s, a, b, c, d):

    a *= s
    b *= s
    c *= s
    d *= s

    context.move_to( 0,   c/2    )
    context.line_to( 0,   c/2 + b)
    context.line_to( d,   0      )
    context.line_to( 0,  -c/2 - b)
    context.line_to( 0,  -c/2    )
    context.line_to(-a,  -c/2    )
    context.line_to(-a,   c/2    )
    context.line_to( 0,   c/2    )   
    context.close_path()
    context.stroke()

    #context.restore()


def square(context,s,a,b):

    a *= s
    b *= s

    context.move_to( -a/2,    a/2 - b    )
    context.line_to(  a/2,    a/2 - b   )
    context.line_to(  a/2,   a/2    )
    context.line_to( -a/2,   a/2    )
    context.line_to( -a/2,    a/2 - b    )
    context.close_path()
    context.stroke()

    # Add text to the square
    #context.set_source_rgb(0, 0, 0)  # Set text color, here it's black. Adjust as needed.
    #context.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    #context.set_font_size(10)  # Set font size. Adjust as needed.
    #x_text = -a/4  # Adjust x position as needed.
    #y_text = 0     # Adjust y position as needed.
    #context.move_to(x_text, y_text)
    #context.show_text('Engine')


def run(shapeID,**argv) :
 
    scale = 300
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, scale, scale)     

    context = cairo.Context(surface)

    context.translate(scale/2, scale/2)

    context.set_line_width(0.035*scale)

    color = argv.setdefault('color',(1,1,1))
    if color[0] == '#':
        """Convert to RGB"""
        color = np.array(hex_to_rgb(color))/255

    context.set_source_rgb(*color)

    # Save the current context state
    context.save()

    # Rotate the context by the given orientation
    orientation = argv.setdefault('orientation',0)
    orientation *=np.pi/180
    context.rotate(-orientation)



    # Call the function
    if shapeID == 'arrow':

     arrow(context,scale,0.4,0.15,0.25,0.2)

    elif shapeID == 'square': 
     aspect_ratio = argv.setdefault('aspect_ratio',0.5)
     
     square(context,scale,1,aspect_ratio)

    else: 
       raise f'No shape recognized {shapeID}' 
    
    
    # Save the drawing to a BytesIO object
    #png_io = BytesIO()
    #surface.write_to_png(png_io)
    #return base64.b64encode(png_io.getvalue()).decode("utf-8")

    buf = BytesIO()
    surface.write_to_png(buf)
    buf.seek(0)
    url = buf.getvalue()
    buf.close()

    return url



 
