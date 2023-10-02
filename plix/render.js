window.addEventListener('load', async function() {

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
    
jsonData = await fetchData();
 if (jsonData) {
        render();
        //updateSlidesVisibility();
} 
  
function updateSlidesVisibility() {
    try {
        var slides = document.querySelectorAll(".slide");
        
        slides.forEach(function(slide, index) {
            if (!slide) {
                console.error('Slide at index:', index, 'not found!');
                return;
            }

            // Using the index directly for comparison with active_slide
            if (window.dataStore.mode === 'presentation' && index !== window.dataStore.active_slide) {
                slide.hidden = true;
            } else {
                slide.hidden = false;
            }
        });
    } catch (error) {
        console.error('Error updating visibility for slides', error);
    }
}

function add_common_properties(element,props) {

     //Style
     if (props.style) {
        for (let styleProp in props.style) {
            let cssValue = props.style[styleProp];
            if (typeof cssValue === 'number' && ['fontSize', 'width', 'height', 'top', 'right', 'bottom', 'left'].includes(styleProp)) {
                cssValue += 'px';
            }
            element.style[styleProp] = cssValue;
        }
    }

    //ClassName
    if (props.className) {
        element.className = props.className;
    }
        
    //Hidden
    if (props.hidden) {
            element.hidden = Boolean(props.hidden);
    }

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


function renderComponent(data,outer_element) {
    let element;
    switch (data.type) {
        case 'Slide':
            element = document.createElement('div');
            add_common_properties(element,data.props)
          
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

            
            add_common_properties(element, data.props);
            outer_element.appendChild(element);
            
            break;
        case 'Img':
                element = document.createElement('img');
                element.src = data.props.src;
                add_common_properties(element,data.props)
                outer_element.appendChild(element)
                break;
        case 'Iframe':
              //Perhaps the external DIV is not necessary here
              element = document.createElement('div')
              add_common_properties(element,data.props)
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
                add_common_properties(element,data.props)
                outer_element.appendChild(element)

                Plotly.newPlot(element, data.props.figure.data, data.props.figure.layout, config);
                break; 

        case 'molecule':

            // Create a new div element
            element = document.createElement("div");
            add_common_properties(element,data.props)
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
 
    // Initialize dataStore if it doesn't exist yet
   if (!window.dataStore) {
    window.dataStore = {};
   }

    //window.dataStore.active_slide = 0;
    window.dataStore.mode = 'presentation';
    window.dataStore.active_slide = 0;

    const slides = document.querySelectorAll(".slide");
    slides.forEach((slide, index) => {
        slide.setAttribute('data-index', index);
        if (index !== 0) {
            slide.hidden = true;}
         else {
            slide.hidden = false;
            console.log('hidden',index)
        }
    });
    

}


})


