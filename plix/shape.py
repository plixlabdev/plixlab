import cairo
import base64
from io import BytesIO
import numpy as np
 
 
def hex_to_rgb(hex_color):
    """
    Convert a hexadecimal color string to an RGB tuple.

    :param hex_color: Hexadecimal color string (e.g., "#FFFFFF")
    :return: RGB tuple
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

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

#     #context.restore()
# def arrow1D(context, x1, y1, x2, y2, arrow_head_length=10, arrow_head_angle=30):
#     """
#     Draws a straight arrow between two coordinates (x1, y1) and (x2, y2).

#     :param context: Cairo context
#     :param x1: Starting x-coordinate
#     :param y1: Starting y-coordinate
#     :param x2: Ending x-coordinate
#     :param y2: Ending y-coordinate
#     :param arrow_head_length: Length of the arrowhead
#     :param arrow_head_angle: Angle of the arrowhead in degrees
#     """
#     # Draw the line part of the arrow
#     context.move_to(x1, y1)
#     context.line_to(x2, y2)
#     context.stroke()

#     # Calculate the direction of the line
#     dx = x2 - x1
#     dy = y2 - y1
#     angle = np.arctan2(dy, dx)

#     # Calculate the arrowhead points
#     left_angle = angle + np.radians(arrow_head_angle)
#     right_angle = angle - np.radians(arrow_head_angle)

#     x_left = x2 - arrow_head_length * np.cos(left_angle)
#     y_left = y2 - arrow_head_length * np.sin(left_angle)

#     x_right = x2 - arrow_head_length * np.cos(right_angle)
#     y_right = y2 - arrow_head_length * np.sin(right_angle)

#     # Draw the arrowhead
#     context.move_to(x2, y2)
#     context.line_to(x_left, y_left)
#     context.stroke()

#     context.move_to(x2, y2)
#     context.line_to(x_right, y_right)
#     context.stroke()


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

    context.set_line_width(0.01*scale)

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
    #if shapeID == 'arrow1D':
    #    start = argv.get('start', (0, 0))
    #    end = argv.get('end', (scale / 2, scale / 2))
        
    #    x1 =  argv.get('x1')
    #    y1 =  argv.get('y1')
    #    x2 =  argv.get('x2')
    #    y2 =  argv.get('y2')
       
    #    arrow1D(context, x1, y1, x2, y2)

    # Call the function
    if shapeID == 'arrow':

     #arrow(context,scale,0.4,0.15,0.25,0.2)
     #(body length,tip width,body width,tip length)
     arrow(context,scale,0.5,0.15,0.25,0.2)


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



 
