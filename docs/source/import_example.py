from docutils import nodes
from docutils.parsers.rst import Directive
import os

"""Rationale: the (binary) example is loaded and passed into an iframe, which wraps around _static/plix"""

class ImportExample(Directive):
    required_arguments = 1
    final_argument_whitespace = True
    has_content = False
    instance_counter = 0  # Class variable to keep track of the number of instances

    def run(self):
        # Increment the instance counter for each object created
        ImportExample.instance_counter += 1

        filename = self.arguments[0]
        print('Example ' + filename)
        print(' ')
        
        #filename_path = os.path.join('_static', filename)

        # Modify iframe ID to include the instance number
        iframe_id = f"iframeExample_{ImportExample.instance_counter}"

        html_content = f'''
<div style="width: 100%; display: block;">
<div class="embed-container wide">
    <iframe id="{iframe_id}" src="_static/web/index.html?suppress_SSE=true" frameborder="0" allowfullscreen style="border:2px solid gray;"></iframe>
</div>
</div>
<div style="height: 1em;"></div>  <!-- spacer added here -->
<script>
document.addEventListener('DOMContentLoaded', function () {{
    const iframe = document.getElementById('{iframe_id}');
    let arrayBuffer = null;
    let iframeLoaded = false;

    function tryPostMessage() {{
        if (iframeLoaded && arrayBuffer) {{
            iframe.contentWindow.postMessage(arrayBuffer, '*');
        }}
    }}

    iframe.addEventListener('load', function () {{
        iframeLoaded = true;
        tryPostMessage();
    }});

    fetch('_static/reference/{filename}.plx')
        .then(response => response.blob())
        .then(blob => {{
            const reader = new FileReader();
            reader.onload = function () {{
                arrayBuffer = this.result;
                tryPostMessage();
            }};
            reader.readAsArrayBuffer(blob);
        }})
        .catch(error => console.error('Error loading file:', error));
}});
</script>
'''
        return [nodes.raw('', html_content, format='html')]


def setup(app):
    app.add_directive('import_example', ImportExample)