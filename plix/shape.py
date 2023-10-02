import cairo
import base64
from io import BytesIO
 
 

# Creating function to make the arrow shape
def arrow(context,s, a, b, c, d):

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

# Creating function to make the arrow shape
def square(context,s,a,b):

    a *= s
    b *= s

    context.move_to( -a/2,   b/2    )
    context.line_to( a/2,   b/2 )
    context.line_to( a/2,   -b/2)
    context.line_to( -a/2,  -b/2    )
    context.line_to( -a/2,   b/2    )
    context.close_path()
    context.stroke()


def run(shapeID,**argv) :
 
    scale = 300
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, scale, scale)     

    context = cairo.Context(surface)

    context.translate(scale/2, scale/2)

    context.set_line_width(0.035*scale)

    color = argv.setdefault('color',(1,1,1))
    context.set_source_rgb(*color)

    # Call the function
    if shapeID == 'arrow':
     arrow(context,scale,0.4,0.15,0.25,0.2)

    elif shapeID == 'square': 
     square(context,scale,0.5,0.5)

    else: 
       raise f'No shape recognized {shapeID}' 
    
    
    # Save the drawing to a BytesIO object
    png_io = BytesIO()
    surface.write_to_png(png_io)

    # Encode as Base64
    return base64.b64encode(png_io.getvalue()).decode("utf-8")



 
