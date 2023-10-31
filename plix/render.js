import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';


 
 // Convert base64 data URL to blob URL
 function dataURItoBlob(dataURI) {
    const byteString = atob(dataURI.split(',')[1]);
    const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]
    const buffer = new ArrayBuffer(byteString.length);
    const dataView = new Uint8Array(buffer);
    for (let i = 0; i < byteString.length; i++) {
        dataView[i] = byteString.charCodeAt(i);
    }
    const blob = new Blob([buffer], { type: mimeString });
    const blobURL = URL.createObjectURL(blob);
    return blobURL;
 }



function import3DModel(modelDataURL,w){


 //Scene
const scene = new THREE.Scene();
// Increase the intensity of the ambient light
const ambientLight = new THREE.AmbientLight(0xffffff, 1); // set intensity to 1
scene.add(ambientLight);

// Increase the intensity of the directional light
const directionalLight = new THREE.DirectionalLight(0xffffff, 2); // set intensity to 2 for stronger light
directionalLight.position.set(1, 2, 4);
scene.add(directionalLight);

// Optionally, add another light source if you want more illumination in your scene
const pointLight = new THREE.PointLight(0xffffff, 1.5, 100); // intensity is 1.5 and distance is 100
pointLight.position.set(-2, 3, -5); // adjust the position as per your needs
scene.add(pointLight);

 //Camera
 const camera = new THREE.PerspectiveCamera(75, 16/9*w, 0.1, 1000);
 camera.position.z = 5;

 //Renderer
 const renderer = new THREE.WebGLRenderer({ alpha: true });
 renderer.setClearColor(0x000000, 0);  // 
 renderer.setSize(window.innerWidth, window.innerHeight);


 const controls = new OrbitControls(camera, renderer.domElement);

 const blobURL = dataURItoBlob(modelDataURL);

 // Now you can use the three.js loader with the blob URL
 const loader = new GLTFLoader();

 
 loader.load(blobURL, function(obj) {
 scene.add( obj.scene );
    
 var box = new THREE.Box3().setFromObject( obj.scene );
 const center = box.getCenter(new THREE.Vector3());

 controls.target.copy(center);
 controls.update(); 
 camera.lookAt(center);

  
 })


 function animate() {
	requestAnimationFrame(animate);
	controls.update();
	renderer.render(scene, camera);
 }

 animate();

 //window.addEventListener('resize', function () {
  //  const newWidth = window.innerWidth;
  //  const newHeight = window.innerHeight;

   // camera.aspect = newWidth / newHeight;
   // camera.updateProjectionMatrix();

    //renderer.setSize(newWidth, newHeight);

    // Make sure the camera still looks at the center of the scene/model
   // camera.lookAt(scene.position);

   // if (controls) {
   //     controls.update();
   // }
//});


return renderer.domElement

}



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
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data.data));
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
    

 const data = await fetchData();

 if (data) {
       const jsonData = data.data
         // Initialize dataStore if it doesn't exist yet
        if (!window.dataStore) {
         window.dataStore = {};
        }

        
        window.dataStore.mode = 'presentation';
        window.dataStore.animation   = data.animation
        
        window.dataStore.index = 0
        window.dataStore.active_slide = 0

        render(jsonData);
        
} 
  


function change_plotly_static(slide,staticc){

    const slideElement = document.getElementById(slide);
    

   // console.log(slideElement)
    const plotlyElements = slideElement.querySelectorAll('.PLOTLY');

    plotlyElements.forEach(element => {
        Plotly.react(element.id, element.data, element.layout, {staticPlot: staticc,responsive: true,scrollZoom: true} );   

    });

}

function add_common_properties(element,data,add_id) {

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
    if (add_id){
    if (data.props.className) {
        element.className = data.props.className;
    }
  
    //ClassName
   
    if (data.id) {
        element.id = data.id;
    }}

}

   
function renderComponent(data,outer_element) {
    let element;
    switch (data.type) {
        case 'Slide':
            element = document.createElement('div');
            add_common_properties(element,data,true)
          
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
          
            
            add_common_properties(element, data,true);

            if (data.props.style.mode === 'hCentered') {
               
                element.style.alignItems = 'center';  // Horizontal centering
                element.style.justifyContent = 'center';  // Vertical centering
            
                // Center-align text for all paragraphs inside the container
                let paragraphs = element.querySelectorAll('p');
                paragraphs.forEach(p => {
                    p.style.textAlign = 'center';
                    p.style.lineHeight = 1.5;
                });
            }
            


            outer_element.appendChild(element);
        
            
  
            //console.log( data.fontsize)
            //==================================================
            function setDynamicFontSize() {
                let fontSize = outer_element.offsetHeight * data.props.fontsize;
                element.style.fontSize = fontSize + 'px';
            }
            
            // Use ResizeObserver to observe size changes on outer_element
            const ro = new ResizeObserver(() => {
                setDynamicFontSize();
            });
            

            let initialBottomPercentage;


            ro.observe(outer_element);
            
            setDynamicFontSize(); // Initial call
            //======================================= 
        


            break;
           

        case 'model3D':
                //element = document.createElement('div');
                //const data = data.props.src;
                const elem = import3DModel(data.props.src,data.props.style.w)
                //element.appendChild(model)

                add_common_properties(elem,data,true)
                outer_element.appendChild(elem)
                break;

        case 'Img':
                element = document.createElement('img');
                element.src = data.props.src;
                add_common_properties(element,data,true)
                outer_element.appendChild(element)
                break;
        case 'Iframe':
              //Perhaps the external DIV is not necessary here
              element = document.createElement('div')
              add_common_properties(element,data,true)
              const iframe = document.createElement('iframe');
              iframe.width = '100%'
              iframe.height = '100%'
              // Set the frameborder to 0
              iframe.setAttribute('frameborder', '0');

              // Enable full screen for various browsers
              //iframe.setAttribute('allowfullscreen', '');
              //iframe.setAttribute('mozallowfullscreen', 'true');
              //iframe.setAttribute('webkitallowfullscreen', 'true');

              // Set other properties
              //iframe.setAttribute('allow', 'autoplay; fullscreen; xr-spatial-tracking');
              //iframe.setAttribute('xr-spatial-tracking', '');
              //iframe.setAttribute('execution-while-out-of-viewport', '');
              //iframe.setAttribute('execution-while-not-rendered', '');
              //iframe.setAttribute('web-share', '');

              iframe.src = data.props.src;


              //manage focus (at the beginning there is no focus on iFrame)
              iframe.tabindex=-1
              iframe.addEventListener('click', function() {
                this.focus();
              });
             
              
              element.appendChild(iframe)
              outer_element.appendChild(element)
              break;     


        case 'Bokeh':

               element = document.createElement('div')
               async function loadBokehFromJson() {
                try {
                    Bokeh.embed.embed_item(data.graph,element);
                } catch (error) {
                    console.error("Error loading Bokeh plot:", error);
                }
              }
    
              loadBokehFromJson();
              add_common_properties(element,data,true)
              outer_element.appendChild(element)
              break; 


        case 'Plotly':
            const config = {
                responsive: true,
                scrollZoom: true,
                staticPlot: false
                //modeBarButtonsToAdd: ["drawline","eraseshape"]
               /// displayModeBar: false
            };
            element = document.createElement('div');
            add_common_properties(element, data,true);
            //TODO: check if this is needed
            element.className = 'PartA interactable PLOTLY'
            outer_element.appendChild(element);

            //Thumbnail
            const thumbnail = document.createElement('img');
            add_common_properties(thumbnail, data,false);
            outer_element.appendChild(thumbnail);
            thumbnail.className = 'PartB interactable'
            thumbnail.id = data.id + 'THUMB'
            thumbnail.style.visibility = 'hidden'
            
            async function generateThumbnail(data, element, thumbnail) {
                try {
                    const gd = await Plotly.react(element, data.props.figure.data, data.props.figure.layout, config);
                    const url = await Plotly.toImage(gd);
            
                    //console.log("Thumbnail URL for", data.id, ":", url);
                    thumbnail.src = url;
            
                } catch (error) {
                    console.error("Error while processing the graph:", error);
                }
            }
            
            // Call the function
            generateThumbnail(data, element, thumbnail);
            
            

           
            break; 

        case 'molecule':

            // Create a new div elementelement
            element = document.createElement("div");
            add_common_properties(element,data,true)
            element.id = "molContainer";  // setting an ID for the container
            outer_element.appendChild(element)
          
            // Initialize the viewer with a background color
            var viewer = $3Dmol.createViewer("molContainer", {
            defaultcolors: $3Dmol.rasmolElementColors,
            backgroundColor: data.props.backgroundColor  
            });

            
            // Fetch the molecule and visualize it
            $3Dmol.download("pdb:" + data.props.structure, viewer, function() {
            viewer.setStyle({stick: {}});
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
   
    return element
    
}

// Adjusted rendering function
function render(jsonData) {

    // Check if jsonData is available
    if (!jsonData) {
        console.error("Data has not been loaded yet!");
        return;
    }
    // Reference to the slide-container
    let container = document.getElementById('slide-container');

 
    jsonData.forEach((data, index) => {
       // console.log("Index:", index);  // This will print the current index
        renderComponent(data, container);
    });

    document.getElementById('loader').classList.remove('loader');

   

    //Run MathJax
    if (window.MathJax) {
        MathJax.typesetPromise();
    }

   
    //Update bar (it works up to 1000 slides)
    const currentUrl = window.location.href
    if (currentUrl.charAt(currentUrl.length - 2) !== '#' &&
    currentUrl.charAt(currentUrl.length - 3) !== '#' &&
    currentUrl.charAt(currentUrl.length - 4) !== '#')  {
     window.location.href += "#" + String(window.dataStore.active_slide);
    } else {
        let parts = currentUrl.split('#');
        let number = parseInt(parts[1], 10);
        window.dataStore.active_slide =number;}


    const active_id = 'S' + String(window.dataStore.active_slide)

    //Update visibility
    const slides = document.querySelectorAll(".slide");
    for (let i = 0; i < slides.length; i++) {
    if (slides[i].id === active_id) {
        
        change_plotly_static(slides[i].id,false)

        slides[i].style.visibility = 'visible';

        
    } else {
        
        change_plotly_static(slides[i].id,true)
        slides[i].style.visibility = 'hidden';
    }
   
   }


}
 


})


