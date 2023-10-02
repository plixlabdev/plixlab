from PIL import Image
import os
import io
import base64
import requests
import plotly.io as pio

def fig_to_base64(fig):
    # Convert fig to PNG Image
    fig_bytes = pio.to_image(fig, format="png")
    # Convert bytes to base64
    base64_string = base64.b64encode(fig_bytes).decode('utf-8')
    return base64_string


def process_plotly(fig):
             """Post processing plotly""" 

             fig.update_layout(
             plot_bgcolor='rgba(0,0,0,0)',
             paper_bgcolor='rgba(0,0,0,0)',
             autosize=True,
             legend=dict(font=dict(color='white')),
             xaxis=dict(
             title=dict(
             font=dict(
                  color='white'
             )
             ),
             tickfont=dict(
             color='white'
             )
             ),
             yaxis=dict(
             title=dict(
             font=dict(
                 color='white'
             )
             ),
             tickfont=dict(
             color='white'
             )
             ) )


             return fig


def get_youtube_thumbnail(videoID):
          #if add_thumbnail:
          url = f"https://img.youtube.com/vi/{videoID}/sddefault.jpg"
          data = requests.get(url).content
          image = Image.open(io.BytesIO(data))
          cropped_image = image.crop((0, 60, 640, 420))

          #add Youtube Logo
          yt_logo = load_icon('youtube')

          # Get the dimensions of the cropped image
          crop_width, crop_height = cropped_image.size

          # Get the dimensions of the yt_logo
          logo_width, logo_height = yt_logo.size

          # Calculate 15% of the cropped image's width
          desired_width = int(crop_width * 0.15)
          # Compute the new height while maintaining the aspect ratio of yt_logo
          desired_height = int((desired_width / yt_logo.width) * yt_logo.height)

          # Resize the yt_logo
          yt_logo_resized = yt_logo.resize((desired_width, desired_height))

          # Compute the x, y position of the yt_logo_resized
          # This will ensure the yt_logo_resized is in the center of the cropped_image
          x_position = (crop_width - desired_width) // 2
          y_position = (crop_height - desired_height) // 2

          # Paste the yt_logo_resized onto the cropped image using its computed x, y position
          # Use the mask for proper pasting if the logo has transparency
          cropped_image.paste(yt_logo_resized, (x_position, y_position), mask=yt_logo_resized.split()[3] if yt_logo_resized.mode == 'RGBA' else None)
          
          #Save the cropped image to bytes
          image_bytes = io.BytesIO()
          cropped_image.save(image_bytes, format='JPEG')
          data = image_bytes.getvalue()
          image_encoded = base64.b64encode(data).decode("utf8")

          return image_encoded


def convert(value):
    return str(value*100) + '%'

def get_style(**style):
        """Format the style"""

        style.update({'position':'absolute'})
        mode = style.setdefault('mode','full')
        if mode == 'manual':
         style.update({'left'  :convert(style.setdefault('x',0))})
         style.update({'bottom':convert(style.setdefault('y',0))})

         if 'w' in style.keys():
             style.update({'width':convert(style['w'])})
            
         if 'h' in style.keys():
             style.update({'height':convert(style['h'])})
     
        elif mode == 'full':

            style['left']   = convert(0)
            style['bottom'] = convert(0)
            style['width']  = convert(1)
            style['height'] = convert(1)

        elif mode == 'hCentered':

            style['bottom'] = convert(style['y'])
            style['textAlign'] = 'center'
            

        elif mode == 'vCentered':


            style['display']         = 'flex'
            style['alignItems']     = 'center'
            style['justifyContent'] = 'center'
            style['height']          = convert(style.setdefault('h',1))
            style['left']   = convert(style.setdefault('x',0))
            if 'w' in style:
              style['width']   = convert(style['w'])

        return style

def hex_to_rgb(hex_color):
    """
    Convert a hexadecimal color string to an RGB tuple.

    :param hex_color: Hexadecimal color string (e.g., "#FFFFFF")
    :return: RGB tuple
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))



def encode_image_to_base64(image):
    """
    Encode a PIL image object to base64 encoded string.

    :param image: PIL image object
    :return: base64 encoded string
    """
    output_image_bytes = io.BytesIO()
    image.save(output_image_bytes, format='PNG')
    base64_encoded_image = base64.b64encode(output_image_bytes.getvalue()).decode('utf8')
    return base64_encoded_image


def change_color(input_image, target_color, new_color, tolerance=50):
    """
    Change a specific color in an image to another color.

    :param input_image: Input PIL image object
    :param target_color: Hexadecimal color string to change (e.g., "#FFFFFF")
    :param new_color: Hexadecimal color string to change to (e.g., "#000000")
    :param tolerance: Optional tolerance for color matching
    :return: PIL image object with changed color
    """
    target_color_rgb = hex_to_rgb(target_color)
   
    new_color_rgb = hex_to_rgb(new_color)
    img = input_image.convert("RGBA")
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = img.getpixel((x, y))
            if abs(r - target_color_rgb[0]) < tolerance and abs(g - target_color_rgb[1]) < tolerance and abs(b - target_color_rgb[2]) < tolerance:
                img.putpixel((x, y), (*new_color_rgb, a))
    return img


def load_icon(appID,background = None):
    """
    Add a background color to an image with a transparent background.

    :param appID: ID of the app 
    :param hex_color: Hexadecimal background color string (e.g., "#FFFFFF")
    """
    #read appID
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
    input_image = os.path.join(script_dir, f"assets/{appID}.png")  # Construct input image path
    img = Image.open(input_image)

    if background:
     img = change_color(img,'#000000',background)
     #bg_color = hex_to_rgb(background)
     #img_new       = Image.new("RGB", img.size, bg_color)
     #img_new.paste(img, mask=img.split()[3])  # Use alpha channel as mask
     #img = img_new

    return img

#def load_icon(appID,background = None):
 #   """
 #   Add a background color to an image with a transparent background.

 #   :param appID: ID of the app 
 #   :param hex_color: Hexadecimal background color string (e.g., "#FFFFFF")
 #   """
 #   #read appID
 #   script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
 #   input_image = os.path.join(script_dir, f"apps/{appID}.png")  # Construct input image path
 #   img = Image.open(input_image)

 #   if background:
 #    bg_color = hex_to_rgb(background)
 #    img_new       = Image.new("RGB", img.size, bg_color)
 #    img_new.paste(img, mask=img.split()[3])  # Use alpha channel as mask
 #    img = img_new

 #   return img

def make_transparent(input_image, hex_color, tolerance=50):
    """
    Make a specific color in an image transparent.

    :param input_image: Input image file path
    :param output_image: Output image file path
    :param hex_color: Hexadecimal color string to make transparent (e.g., "#FFFFFF")
    :param tolerance: Optional tolerance for color matching
    """

    target_color = hex_to_rgb(hex_color)
    input_image = Image.open(input_image)
    img = input_image.convert("RGBA")
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = img.getpixel((x, y))
            if abs(r - target_color[0]) < tolerance and abs(g - target_color[1]) < tolerance and abs(b - target_color[2]) < tolerance:
                img.putpixel((x, y), (r, g, b, 0))

    return img            
    #img.save(output_image, "PNG")

# Example usage
#input_image = "optart_thumbnail.png"  # Input image file path
#output_image = "output.png"  # Output image file path
#hex_color = "#94A684" # Hexadecimal color string to make transparent
#tolerance = 50  # Optional tolerance for color matching

#make_transparent(input_image, output_image, hex_color, tolerance)

