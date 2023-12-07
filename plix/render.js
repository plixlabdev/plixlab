import * as THREE from 'three';
import { GLTFLoader } from './assets/js/GLTFLoader.js'
import { OrbitControls } from './assets/js/OrbitControls.js'
//import * as jsonpatch from './assets/js/fast-json-patch/index.mjs';

 
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
//const scene = new Scene();
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
 //const loader = new THREE.GLTFLoader();


 
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



return renderer.domElement

}


window.addEventListener('load', async function() {

    let isFirstConnection = true;
  
    
    function connectWebSocket() {
     
    
        try {
            const ws = new WebSocket(`ws://localhost:8888/data?isFirstConnection=${isFirstConnection}`);
    
            ws.onopen = function(event) {
                console.log("Connected to WebSocket.");
                isFirstConnection = false; // Reset the flag after establishing the connection
               
            };
    
            ws.onmessage = function(event) {
                console.log("Message received.");
                render_presentation(JSON.parse(event.data));
            };
    
            ws.onerror = function(event) {
                console.error("WebSocket error observed. Attempting to reconnect...");
                // Do not initiate reconnect here, let onclose handle it
            };
    
            ws.onclose = function(event) {
                console.log("WebSocket connection closed. Attempting to reconnect...");
              
                setTimeout(connectWebSocket, 1000); // Exponential backoff
            };
        } catch (error) {
            setTimeout(connectWebSocket, 1000); // Exponential backoff
        }
    }
    
    connectWebSocket();
    

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

   
    
async function render_presentation(data) {
   
    if (data) {
        const jsonData = data.patch;
        console.log(jsonData)
        
        if (jsonData.length > 0){
    
           // Initialize dataStore if it doesn't exist yet
           if (!window.dataStore) {
            window.dataStore = {
                animation: {},
                index: 0,
                active_slide: 0,
                mode: 'presentation',
                presentation: {}
            };
           } 

            // Apply patch
            console.log('Applying patch', jsonData, ' to ' ,window.dataStore.presentation );
            try {
                const patchResult = jsonpatch.applyPatch(window.dataStore.presentation, jsonData);
                window.dataStore.presentation = patchResult.newDocument;
                console.log('Patch applied successfully. New document: ', patchResult.newDocument);
            } catch (error) {
                console.error('Error applying JSON patch:', error);
            }
        

        // Render the presentation
        render_patch(jsonData);
        }
    } else {
        console.log('No data received to render the presentation.');
    }
}


// Since render_presentation is async, it returns a Promise.
// You can use .then() and .catch() to handle the resolved value or any errors.
render_presentation(false)
    .then(() => {
        console.log('Presentation rendered successfully.');
    })
    .catch(error => {
        console.error('Error in rendering presentation:', error);
    }); 


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

function apply_style(element,style) {

    //Style
    for (let styleProp in style) {
           let cssValue = style[styleProp];
           if (typeof cssValue === 'number' && ['fontSize', 'width', 'height', 'top', 'right', 'bottom', 'left'].includes(styleProp)) {
               cssValue += 'px';
           }
           element.style[styleProp] = cssValue;
    }
   
}


   

function update_markdown(element,field,value){
    //Update Markdown
   // console.log(field)
     //Build markdown formatter--
    const markedInstance = marked.setOptions({
    langPrefix: 'hljs language-',
    highlight: function(code, lang) {
      const language = hljs.getLanguage(lang) ? lang : 'plaintext';
      return hljs.highlight(code, { language }).value;
    }
    });

    if (field === 'text'){element.innerHTML =  markedInstance(value);}

    if (field === 'style'){
        apply_style(element, value);
    
        if (value.alignItems === 'center' & value.justifyContent === 'center') {

         // Center-align text for all paragraphs inside the container
         let paragraphs = element.querySelectorAll('p');
         paragraphs.forEach(p => {
            p.style.textAlign = 'center';
            p.style.lineHeight = 1.5;
         });
      }
    }

    if (field === 'fontsize'){

     function set_fontsize(element,newFontsize){

     let outer_element = element.parentElement

     //==================================================
     function setDynamicFontSize() {
         let fontSize = outer_element.offsetHeight * newFontsize;
         element.style.fontSize = fontSize + 'px';
     }
    
     // Use ResizeObserver to observe size changes on outer_element
     const ro = new ResizeObserver(() => {
        setDynamicFontSize();
     });
    

        // Disconnect the existing observer if it exists
      if (element.ResizeObserver) {
        element.ResizeObserver.disconnect();
      }

     ro.observe(outer_element);   
    
     element.ResizeObserver = ro;
         
     setDynamicFontSize(); // Initial call
     //======================================= 
     }

     set_fontsize(element,value)
    }

}


function add_markdown(id,outer_element){

    const element = document.createElement('div')
    element.className = 'markdownComponent interactable componentA'
    element.id = id
    
    return element
}

function renderComponent(data,outer_element) {
    let element;
    switch (data.type) {
       
        case 'Markdown':

            //Text
            element = add_markdown(data.id)
            outer_element.appendChild(element)
            update_markdown(element,'text',data.text)
            update_markdown(element,'style',data.style)
            update_markdown(element,'fontsize',data.fontsize)
            
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
            //element.id = "molContainer";  // setting an ID for the container
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
    
   
      return element
    
}


function render_slides(slides,container){

    for (const slide in slides) {


        //create slide
        let element = document.createElement('div');
        element.className = 'slide';
        element.id = slide
        element.style.backgroundColor = slides[slide].style.backgroundColor
        container.appendChild(element)
        //------
        
        //render elements--
        for (const key in slides[slide]['children']){

            let component = renderComponent(slides[slide]['children'][key],element)
            component.id = key
            
        }

        //update animation
        window.dataStore.animation[slide] = slides[slide]['animation'] 

    }
}


function update_component(component_ID,field,value)
{

    const element = document.getElementById(component_ID)
    const className = element.className

    if (className.includes('markdownComponent')){
        update_markdown(element,field,value)
    }

}

function add_component(id,data,outer_element){
   
    if (data.type === 'Markdown'){
     
        const element = add_markdown(id)
        outer_element.appendChild(element)
        update_markdown(element,'text',data.text)
        update_markdown(element,'style',data.style)
        update_markdown(element,'fontsize',data.fontsize)

    }

}


// Adjusted rendering function
function render_patch(jsonData) {
   
    // Reference to the slide-container
    let container = document.getElementById('slide-container');

    //const jsonData = window.dataStore.presentation.slides
    //console.log(jsonData)
    for (const key in jsonData) {

       const patch = jsonData[key]
       if (!patch.path.split('/').includes('animation')) {
        
         //Render the whole presentation--
         if (patch.op === 'add'){
           if (patch.path === '/slides'){
           //Add slides 
           render_slides(patch.value,container)
           }

          if (patch.path.split('/')[3] === 'children'){
          //Add component  
           const component_ID = patch.path.split('/')[4]
           const value = patch.value  
           add_component(component_ID,value,container)
          }
        }

    
        if (patch.op === 'remove'){
            
            if (patch.path.split('/')[3] === 'children'){
                const component_ID = patch.path.split('/')[4]
                document.getElementById(component_ID).remove();
            } 
            //console.log(component_ID)
            

           // console.log('op ' + patch.op + ' path ' + patch.path + ' value ' + patch.value)
        }

       if (patch.op === 'replace'){
        //[{'op': 'replace', 'path': '/slides/S0/children/S0_C0/children', 'value': 'fkk '}]
        
        const component_ID = patch.path.split('/')[4]
        const field = patch.path.split('/')[5]
        const value = patch.value
        
        update_component(component_ID,field,value)

       }

    }  
    }


   

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


// Adjusted rendering function
function render(jsonData) {

    // Check if jsonData is available
    if (!jsonData) {
        console.error("Data has not been loaded yet!");
        return;
    }
    // Reference to the slide-container
    let container = document.getElementById('slide-container');

    //const title   = jsonData['title']



    for (const slide in jsonData) {

        //create slide
        let element = document.createElement('div');
        element.className = 'slide';
        element.id = slide
        element.style.backgroundColor = jsonData[slide].style.backgroundColor
        container.appendChild(element)
        
        //render elements--
        for (const key in jsonData[slide]['children']){

            let component = renderComponent(jsonData[slide]['children'][key],element)
            component.id = key
            
        }


    }
 
  
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


