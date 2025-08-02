#!/usr/bin/env python3
"""
Remove third-party assets from web directory.
This script removes all third-party libraries from the web assets directory,
keeping only PlixLab's own files.
"""

import os
import shutil
from pathlib import Path

def get_web_assets_dir():
    """Get the web assets directory."""
    return Path(__file__).parent / "web" / "assets"

def backup_and_remove_third_party():
    """Remove third-party assets, creating a backup first."""
    assets_dir = get_web_assets_dir()
    js_dir = assets_dir / "js"
    css_dir = assets_dir / "css"
    
    # Create backup directory
    backup_dir = Path(__file__).parent / "web_assets_backup"
    backup_dir.mkdir(exist_ok=True)
    
    # Third-party JavaScript files to remove
    third_party_js = [
        "3Dmol-min.js", "3Dmol.js", "3Dmol.ui-min.js",
        "BufferGeometryUtils.js", "GLTFLoader.js", "OrbitControls.js",
        "bokeh-3.6.2.min.js", "bokeh-api-3.6.2.min.js", "bokeh-gl-3.6.2.min.js",
        "bokeh-tables-3.6.2.min.js", "bokeh-widgets-3.6.2.min.js",
        "clipboard.min.js", "fast-json-patch.js", "fast-json-patch.min.js",
        "highlight.min.js", "index.umd.js", "jsonpatch.js", "jsonpatch.min.js",
        "marked.min.js", "msgpackr.js", "plotly-3.0.1.min.js", "pyodide.js",
        "rfc6902.js", "rfc6902.min.js", "tex-mml-chtml.js", "tex-mml-chtml.js.1",
        "three.min.js", "three.module.js", "webpack.config.js"  # Added unused webpack config
    ]
    
    # PlixLab's own files that should NOT be removed
    plixlab_own_files = [
        "plixlab.js", "models.js", "load.js", "local_only.js"
    ]
    
    # Third-party CSS files to remove
    third_party_css = [
        "all.min.css", "bootstrap.min.css", "bootstrap.min.css.map", "dark.min.css"
    ]
    
    # Third-party directories to remove
    third_party_dirs = [
        "input", "output"  # MathJax directories
    ]
    
    # Backup and remove JS files
    for filename in third_party_js:
        # Safety check: make sure we're not removing PlixLab's own files
        if filename in plixlab_own_files:
            print(f"SAFETY CHECK: Skipping {filename} (it's a PlixLab file)")
            continue
            
        source = js_dir / filename
        if source.exists():
            backup = backup_dir / f"js_{filename}"
            shutil.copy2(source, backup)
            source.unlink()
            print(f"Removed and backed up: {filename}")
        else:
            print(f"File not found (already removed?): {filename}")
    
    # Backup and remove CSS files
    for filename in third_party_css:
        source = css_dir / filename
        if source.exists():
            backup = backup_dir / f"css_{filename}"
            shutil.copy2(source, backup)
            source.unlink()
            print(f"Removed and backed up: {filename}")
    
    # Backup and remove third-party directories
    for dirname in third_party_dirs:
        source = js_dir / dirname
        if source.exists():
            backup = backup_dir / f"dir_{dirname}"
            shutil.copytree(source, backup)
            shutil.rmtree(source)
            print(f"Removed and backed up directory: {dirname}")
    
    # Backup and remove webfonts directory
    webfonts_dir = assets_dir / "webfonts"
    if webfonts_dir.exists():
        backup = backup_dir / "dir_webfonts"
        shutil.copytree(webfonts_dir, backup)
        shutil.rmtree(webfonts_dir)
        print(f"Removed and backed up directory: webfonts")
    
    print(f"\nThird-party assets backed up to: {backup_dir}")
    print("Your PlixLab files remain in the web/assets directory:")
    
    # List remaining files
    print("\nRemaining JS files:")
    for f in js_dir.glob("*.js"):
        is_plixlab_file = f.name in plixlab_own_files
        status = "(PlixLab file)" if is_plixlab_file else "(Unknown - check if this should be removed)"
        print(f"  - {f.name} {status}")
    
    print("\nRemaining CSS files:")
    for f in css_dir.glob("*.css"):
        is_plixlab_file = f.name == "plixlab.css"
        status = "(PlixLab file)" if is_plixlab_file else "(Unknown - check if this should be removed)"
        print(f"  - {f.name} {status}")
    
    print(f"\nPlixLab's own files that were preserved:")
    for filename in plixlab_own_files:
        if (js_dir / filename).exists():
            print(f"  ✓ {filename}")
    if (css_dir / "plixlab.css").exists():
        print(f"  ✓ plixlab.css")

if __name__ == "__main__":
    backup_and_remove_third_party()
