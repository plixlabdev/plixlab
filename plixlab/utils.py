"""
PlixLab Utilities Module
"""


from typing import Any, Dict,Union,List
from bokeh.plotting import figure as bokeh_figure



def normalize_dict(data: Any) -> Any:
    """
    Recursively normalize a dictionary, list, or tuple for serialization.

    This function ensures that complex nested data structures can be properly
    serialized by converting them to basic Python types.

    Args:
        data: Data structure to normalize (dict, list, tuple, or other)

    Returns:
        Normalized data structure with the same content but serializable types
    """
    if isinstance(data, dict):
        return {k: normalize_dict(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [normalize_dict(v) for v in data]
    else:
        return data


def process_bokeh(fig: bokeh_figure) -> None:
    """
    Apply PlixLab styling to a Bokeh figure for consistent presentation appearance.

    Configures the figure with white text on transparent background to match
    the PlixLab presentation theme.

    Args:
        fig: Bokeh figure object to style

    Note:
        Modifies the figure in-place
    """
    fig.xaxis.major_tick_line_color = "white"
    fig.xaxis.major_label_text_color = "white"
    fig.yaxis.major_tick_line_color = "white"
    fig.yaxis.major_label_text_color = "white"
    fig.xaxis.axis_label_text_color = "white"
    fig.yaxis.axis_label_text_color = "white"
    fig.background_fill_color = None
    fig.border_fill_color = None
    fig.sizing_mode = "stretch_both"


def process_plotly(fig: Any) -> Any:
    """
    Apply PlixLab styling to a Plotly figure for consistent presentation appearance.

    Configures the figure with white text on transparent background and disables
    interaction features to match the PlixLab presentation theme.

    Args:
        fig: Plotly figure object to style

    Returns:
        Plotly figure object: The styled figure
    """
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        legend=dict(font=dict(color="white")),
        xaxis=dict(title=dict(font=dict(color="white")), tickfont=dict(color="white")),
        yaxis=dict(title=dict(font=dict(color="white")), tickfont=dict(color="white")),
        dragmode=None,
    )

    return fig



def get_style(x: float, y: float, w: float, h: Union[float,str], 
                 halign: str, valign: str) -> Dict[str, str]:
        """ Generate CSS style for a component based on its position and size.

        Args:
            x (float): Horizontal position (0-1, left to right).
            y (float): Vertical position (0-1, bottom to top).
            w (float): Width (0-1, relative to slide).
            h (Union[float,str]): Height (0-1, relative to slide or 'auto').
            halign (str): Horizontal alignment ('left', 'center', 'right').
            valign (str): Vertical alignment ('top', 'center', 'bottom').

        Returns:
            Dict[str, str]: CSS style properties.
        """
        
        style = {}

        if halign == "center":
            tx = -0.5
        elif halign == "left": 
            tx = 0   
        elif halign == "right":
            tx = -1
        else:
            raise ValueError(f"Invalid horizontal alignment: {halign}")    

        if valign == "center":
            ty = 0.5
        elif valign == "top":
            ty = 1    
        elif valign == "bottom":
            ty = 0
        else:
            raise ValueError(f"Invalid vertical alignment: {valign}")
        
           
        style = { 'position': 'absolute',
                  'left':     f'{x*100}%', 
                  'bottom':   f'{y*100}%', 
                  'transform': f'translate({tx*100}%,{ty*100}%)',                  
        }

        
        style['width'] = f'{w*100}%' if w is not None else 'auto'

        if not h == 'auto':
            style['height'] = f'{h*100}%'
        else:
            style['height'] = 'auto'    


        return style

