window.addEventListener('load', async function() {

   
//Reload
const ws = new WebSocket('ws://localhost:8888/reload');

ws.onmessage = function(event) {
    if(event.data === "reload") {
        pollServerAndReload();
    }
};

function pollServerAndReload() {
    fetch("/ping")
    .then(response => {
        if(response.ok) {
            location.reload();
        } else {
            setTimeout(pollServerAndReload, 100);  // Wait 500ms and then try again
        }
    })
    .catch(() => {
        // If there was an error (like the server being down), wait a bit and then try again
        setTimeout(pollServerAndReload, 500);
    });
}
document.getElementById('share').addEventListener('click', function() {
    fetch("/share")
        .then(response => response.text())
        .then(url => {
            console.log(url);
            showModal(url);
        })
        .catch(error => {
            console.error("Error fetching share URL:", error);
        });
});

// Initialize clipboard
const clipboard = new ClipboardJS('#copyBtn');

clipboard.on('success', function(e) {
    const modalText = document.getElementById('modalText');
    modalText.textContent = "Copied to clipboard!";
    
    setTimeout(() => {
        closeModal(); // Close the modal after 1.5 seconds
    }, 1500);
    
    e.clearSelection();
});


function showModal(text) {
    const modal = document.getElementById('customModal');
    const modalText = document.getElementById('modalText');
    const copyBtn = document.getElementById('copyBtn');

    modalText.textContent = text;
    copyBtn.setAttribute('data-clipboard-text', text); // set the clipboard text for the button
    modal.style.display = 'block';

    // This will close the modal if you click outside of it
    window.onclick = function(event) {
        if (event.target === modal) {
            closeModal();
        }
    }
}

function closeModal() {
    const modal = document.getElementById('customModal');
    modal.style.display = 'none';
}




function downloadJSONData() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(jsonData));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "presentation.plx");
    document.body.appendChild(downloadAnchorNode); 
    downloadAnchorNode.click(); 
    downloadAnchorNode.remove();
}

document.getElementById('download').addEventListener('click', function() {
    downloadJSONData();
});

   
   
    async function fetchData() {
        try {
            const response = await fetch('/data');
    
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            return await response.json();
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }
    

 data = await fetchData();

 if (data) {
        jsonData = data.data
        //console.log(data.animation)
         // Initialize dataStore if it doesn't exist yet
        if (!window.dataStore) {
         window.dataStore = {};
        }

        //window.dataStore.active_slide = 0;
        window.dataStore.mode = 'presentation';
        //window.dataStore.active_slide = 0;
        window.dataStore.animation   = data.animation
        
        window.dataStore.index = 0
        window.dataStore.active_slide = 0

        render();
        //updateVisibility();
} 
  

function add_common_properties(element,data) {

     //Style
     if (data.props.style) {
        for (let styleProp in data.props.style) {
            let cssValue = data.props.style[styleProp];
            if (typeof cssValue === 'number' && ['fontSize', 'width', 'height', 'top', 'right', 'bottom', 'left'].includes(styleProp)) {
                cssValue += 'px';
            }
            element.style[styleProp] = cssValue;
        }
    }

    //ClassName
    if (data.props.className) {
        element.className = data.props.className;
    }
        
    //Hidden
    if (data.props.hidden) {
            element.hidden = Boolean(data.props.hidden);
    }

    //ClassName
    if (data.id) {
        element.id = data.id;
    }

}


function renderComponent(data,outer_element) {
    let element;
    switch (data.type) {
        case 'Slide':
            element = document.createElement('div');
            add_common_properties(element,data)
          
            outer_element.appendChild(element)
            break;
        case 'Markdown':

            //Build markdown formatter--
         const markedInstance = marked.setOptions({
          langPrefix: 'hljs language-',
          highlight: function(code, lang) {
            const language = hljs.getLanguage(lang) ? lang : 'plaintext';
            return hljs.highlight(code, { language }).value;
          }
          });
       
         
            element = document.createElement('div')
            const text = markedInstance(data.props.children);
            element.innerHTML = text
            
            add_common_properties(element, data);
            outer_element.appendChild(element);
            
            break;
        case 'Img':
                element = document.createElement('img');
                element.src = data.props.src;
                add_common_properties(element,data)
                outer_element.appendChild(element)
                break;
        case 'Iframe':
              //Perhaps the external DIV is not necessary here
              element = document.createElement('div')
              add_common_properties(element,data)
              iframe = document.createElement('iframe');
              iframe.width = '100%'
              iframe.height = '100%'

              iframe.src = data.props.src;            
              element.appendChild(iframe)
              
              outer_element.appendChild(element)
              break;     
        case 'Graph':
                const config = {
                    responsive: true
                };
                element = document.createElement('div');
                add_common_properties(element,data)
                outer_element.appendChild(element)
                
                 
                requestAnimationFrame(function() {
                    Plotly.newPlot(element, data.props.figure.data, data.props.figure.layout, config);
                });
        
                break; 

        case 'molecule':

            // Create a new div element
            element = document.createElement("div");
            add_common_properties(element,data)
            element.id = "molContainer";  // setting an ID for the container
            outer_element.appendChild(element)
          
            // Initialize the viewer with a background color
            var viewer = $3Dmol.createViewer("molContainer", {
            defaultcolors: $3Dmol.rasmolElementColors,
            backgroundColor: data.props.backgroundColor  
            });

            
            // Fetch the molecule and visualize it
            $3Dmol.download("pdb:" + data.props.structure, viewer, function() {
            viewer.setStyle({}, {stick: {}});
            viewer.zoomTo();
            viewer.render();
           });
               

          break;

        default:
            return;   
        }
    
    
     // Assign properties from the JSON to the created element
    for (let prop in data.props) {

       if (prop === 'children' && Array.isArray(data.props[prop])) {
        data.props[prop].forEach(childData => {

            let childElement = renderComponent(childData,element);
             if (childElement) {
               element.appendChild(childElement);
              }
        });
    }
    }
   
    
    
}

// Adjusted rendering function
function render() {

    // Check if jsonData is available
    if (!jsonData) {
        console.error("Data has not been loaded yet!");
        return;
    }
    // Reference to the slide-container
    let container = document.getElementById('slide-container');

    // Render the components based on JSON data
    jsonData.forEach((data) => {
        renderComponent(data,container);
    });

    document.getElementById('S' + String(window.dataStore.active_slide)).hidden=false;
    

}


})


