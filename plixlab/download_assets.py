#!/usr/bin/env python3
"""
Download third-party assets for PlixLab web interface.
This script downloads the required third-party JavaScript and CSS libraries
that are needed for PlixLab to function properly.
"""

import os
import urllib.request
import shutil
from pathlib import Path

def get_web_assets_dir():
    """Get the web assets directory relative to this module."""
    current_dir = Path(__file__).parent
    return current_dir / "web" / "assets"

def download_file(url, destination):
    """Download a file from URL to destination with verification."""
    print(f"Downloading {url} -> {destination}")
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    try:
        # Download the file
        urllib.request.urlretrieve(url, destination)
        
        # Verify the download for critical JavaScript files
        if destination.name.endswith('.js'):
            with open(destination, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(100)  # Read first 100 chars
                if content.strip().startswith('<!DOCTYPE') or content.strip().startswith('<html'):
                    # File contains HTML instead of JavaScript - this is an error page
                    print(f"Warning: {destination.name} contains HTML instead of JavaScript")
                    print("This usually means the CDN returned an error page")
                    os.remove(destination)  # Remove the bad file
                    raise ValueError(f"Downloaded file {destination.name} contains HTML error page")
        
        print(f"Successfully downloaded {destination.name}")
        
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        raise

def download_mathjax_components(js_dir):
    """Download MathJax input and output components."""
    # Create MathJax directories
    input_dir = js_dir / "input" / "tex" / "extensions"
    output_dir = js_dir / "output" / "chtml" / "fonts" / "woff-v2"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # MathJax TeX extensions
    mathjax_input = {
        "boldsymbol.js": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/input/tex/extensions/boldsymbol.js",
        "color.js": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/input/tex/extensions/color.js",
    }
    
    # MathJax fonts (these are quite a few, so we'll download the main ones)
    mathjax_fonts = {
        "MathJax_AMS-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_AMS-Regular.woff",
        "MathJax_Calligraphic-Bold.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Calligraphic-Bold.woff",
        "MathJax_Calligraphic-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Calligraphic-Regular.woff",
        "MathJax_Fraktur-Bold.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Fraktur-Bold.woff",
        "MathJax_Fraktur-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Fraktur-Regular.woff",
        "MathJax_Main-Bold.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Main-Bold.woff",
        "MathJax_Main-Italic.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Main-Italic.woff",
        "MathJax_Main-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Main-Regular.woff",
        "MathJax_Math-BoldItalic.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Math-BoldItalic.woff",
        "MathJax_Math-Italic.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Math-Italic.woff",
        "MathJax_Math-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Math-Regular.woff",
        "MathJax_SansSerif-Bold.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_SansSerif-Bold.woff",
        "MathJax_SansSerif-Italic.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_SansSerif-Italic.woff",
        "MathJax_SansSerif-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_SansSerif-Regular.woff",
        "MathJax_Script-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Script-Regular.woff",
        "MathJax_Size1-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Size1-Regular.woff",
        "MathJax_Size2-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Size2-Regular.woff",
        "MathJax_Size3-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Size3-Regular.woff",
        "MathJax_Size4-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Size4-Regular.woff",
        "MathJax_Typewriter-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Typewriter-Regular.woff",
        "MathJax_Vector-Bold.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Vector-Bold.woff",
        "MathJax_Vector-Regular.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Vector-Regular.woff",
        "MathJax_Zero.woff": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2/MathJax_Zero.woff",
    }
    
    # Download input extensions
    for filename, url in mathjax_input.items():
        download_file(url, input_dir / filename)
    
    # Download fonts
    for filename, url in mathjax_fonts.items():
        download_file(url, output_dir / filename)

def download_assets():
    """Download all required third-party assets."""
    assets_dir = get_web_assets_dir()
    js_dir = assets_dir / "js"
    css_dir = assets_dir / "css"
    
    # Create directories
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)
    webfonts_dir = assets_dir / "webfonts"
    webfonts_dir.mkdir(parents=True, exist_ok=True)
    
    # Third-party JavaScript libraries
    js_downloads = {
        # Three.js for 3D rendering
        "three.min.js": "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js",
        "three.module.js": "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.js",
        
        # Three.js addons (ES6 modules from JSM path)
        "GLTFLoader.js": "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/jsm/loaders/GLTFLoader.js",
        "OrbitControls.js": "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/jsm/controls/OrbitControls.js",
        "BufferGeometryUtils.js": "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/jsm/utils/BufferGeometryUtils.js",
        
        # 3DMol.js for molecular visualization (using unpkg which has reliable downloads)
        "3Dmol-min.js": "https://unpkg.com/3dmol@2.5.2/build/3Dmol-min.js",
        "3Dmol.js": "https://unpkg.com/3dmol@2.5.2/build/3Dmol.js",
        
        # Plotly for interactive plots
        "plotly-3.0.1.min.js": "https://cdn.plot.ly/plotly-3.0.1.min.js",
        
        # Bokeh for interactive plots (version 3.6.2 to match your dependency)
        "bokeh-3.6.2.min.js": "https://cdn.bokeh.org/bokeh/release/bokeh-3.6.2.min.js",
        "bokeh-api-3.6.2.min.js": "https://cdn.bokeh.org/bokeh/release/bokeh-api-3.6.2.min.js",
        "bokeh-gl-3.6.2.min.js": "https://cdn.bokeh.org/bokeh/release/bokeh-gl-3.6.2.min.js",
        "bokeh-tables-3.6.2.min.js": "https://cdn.bokeh.org/bokeh/release/bokeh-tables-3.6.2.min.js",
        "bokeh-widgets-3.6.2.min.js": "https://cdn.bokeh.org/bokeh/release/bokeh-widgets-3.6.2.min.js",
        
        # Utility libraries
        "marked.min.js": "https://cdnjs.cloudflare.com/ajax/libs/marked/4.3.0/marked.min.js",
        "highlight.min.js": "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js",
        "clipboard.min.js": "https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.11/clipboard.min.js",
        "msgpackr.js": "https://cdn.jsdelivr.net/npm/msgpackr@1.10.1/dist/index.js",
        
        # JSON Patch libraries
        "fast-json-patch.min.js": "https://cdnjs.cloudflare.com/ajax/libs/fast-json-patch/3.1.1/fast-json-patch.min.js",
        "fast-json-patch.js": "https://cdnjs.cloudflare.com/ajax/libs/fast-json-patch/3.1.1/fast-json-patch.js",
        "jsonpatch.min.js": "https://cdnjs.cloudflare.com/ajax/libs/jsonpatch/0.5.4/jsonpatch.min.js",
        "jsonpatch.js": "https://cdnjs.cloudflare.com/ajax/libs/jsonpatch/0.5.4/jsonpatch.js",
        "rfc6902.min.js": "https://cdn.jsdelivr.net/npm/rfc6902@5.0.1/dist/rfc6902.min.js",
        "rfc6902.js": "https://cdn.jsdelivr.net/npm/rfc6902@5.0.1/dist/rfc6902.js",
        
        # MathJax for LaTeX rendering
        "tex-mml-chtml.js": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js",
        
        # Pyodide for Python in browser
        "pyodide.js": "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js",
    }
    
    # Third-party CSS libraries
    css_downloads = {
        # Bootstrap
        "bootstrap.min.css": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css",
        "bootstrap.min.css.map": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css.map",
        
        # Font Awesome
        "all.min.css": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
        
        # Highlight.js theme
        "dark.min.css": "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/dark.min.css",
    }
    
    # Font Awesome webfonts
    webfont_downloads = {
        "fa-regular-400.woff2": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/webfonts/fa-regular-400.woff2",
        "fa-regular-400.ttf": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/webfonts/fa-regular-400.ttf",
        "fa-solid-900.woff2": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/webfonts/fa-solid-900.woff2",
        "fa-solid-900.ttf": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/webfonts/fa-solid-900.ttf",
    }
    
    # Download JavaScript files
    for filename, url in js_downloads.items():
        destination = js_dir / filename
        try:
            download_file(url, destination)
        except Exception as e:
            print(f"Warning: Could not download {filename}: {e}")
            
            # For critical 3DMol.js and Three.js files, try alternative sources
            if filename == "3Dmol-min.js":
                print("Trying alternative CDN for 3Dmol-min.js...")
                try:
                    alt_url = "https://3dmol.csb.pitt.edu/build/3Dmol-min.js"
                    download_file(alt_url, destination)
                except Exception as e2:
                    print(f"Alternative download also failed: {e2}")
            
            elif filename.startswith("GLTFLoader") or filename.startswith("OrbitControls") or filename.startswith("BufferGeometry"):
                print(f"Trying direct GitHub source for {filename}...")
                try:
                    # Use direct GitHub raw files as fallback
                    github_base = "https://raw.githubusercontent.com/mrdoob/three.js/r128/examples/jsm/"
                    if "GLTFLoader" in filename:
                        alt_url = github_base + "loaders/GLTFLoader.js"
                    elif "OrbitControls" in filename:
                        alt_url = github_base + "controls/OrbitControls.js"
                    elif "BufferGeometry" in filename:
                        alt_url = github_base + "utils/BufferGeometryUtils.js"
                    download_file(alt_url, destination)
                except Exception as e2:
                    print(f"GitHub fallback also failed: {e2}")
    
    # Download CSS files
    for filename, url in css_downloads.items():
        try:
            download_file(url, css_dir / filename)
        except Exception as e:
            print(f"Warning: Could not download {filename}: {e}")
    
    # Download webfont files
    for filename, url in webfont_downloads.items():
        try:
            download_file(url, webfonts_dir / filename)
        except Exception as e:
            print(f"Warning: Could not download {filename}: {e}")
    
    # Download MathJax components
    try:
        download_mathjax_components(js_dir)
    except Exception as e:
        print(f"Warning: Could not download MathJax components: {e}")
    
    # Copy webpack config if it doesn't exist (this might be yours)
    webpack_config = js_dir / "webpack.config.js"
    if not webpack_config.exists():
        print(f"Note: webpack.config.js not downloaded - assuming it's your file")
    
    print("Asset download completed!")

if __name__ == "__main__":
    download_assets()
