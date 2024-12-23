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

        # Embeds an iframe that will be the target for the postMessage
        html_content = f'''
<div class="embed-container">
    <iframe id="{iframe_id}" src="_static/index.html?suppress_SSE=true" frameborder="0" allowfullscreen style="border:2px solid gray;"></iframe>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {{
    fetch('_static/{filename}.plx')
        .then(response => response.blob()) // Fetch the file as Blob
        .then(blob => {{
            const reader = new FileReader();
            reader.onload = function() {{
                const arrayBuffer = this.result;
                const iframe = document.getElementById('{iframe_id}');
                iframe.onload = () => iframe.contentWindow.postMessage(arrayBuffer, '*'); // Send the ArrayBuffer
            }};
            reader.readAsArrayBuffer(blob); // Read the Blob as ArrayBuffer
        }})
        .catch(error => console.error('Error loading file:', error));
}});
</script>
'''
        return [nodes.raw('', html_content, format='html')]


def setup(app):
    app.add_directive('import_example', ImportExample)
