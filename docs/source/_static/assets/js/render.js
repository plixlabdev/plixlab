import {import3DModel} from './models.js';



    
export async function render_presentation(jsonData) {
   
    console.log(jsonData)
    if (jsonData) {
       
        if (jsonData.length > 0){
    
           // Initialize dataStore if it doesn't exist yet
           //if (!window.dataStore) {
           // window.dataStore = {
            //    animation: {},
            //    index: 0,
            ///    active_slide: 0,
             //   mode: 'presentation',
                presentation: {}
            //};
           //} 

            // Apply patch
            try {
                const patchResult = jsonpatch.applyPatch(window.dataStore.presentation, jsonData);
                window.dataStore.presentation = patchResult.newDocument;
              //  console.log('Patch applied successfully. New document: ', patchResult.newDocument);
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
//render_presentation(false)
//    .then(() => {
 //       console.log('Presentation rendered successfully.');
 //   })
 //   .catch(error => {
 //       console.error('Error in rendering presentation:', error);
 //   }); 




// Adjusted rendering function
function render_data(jsonData) {
   

    // Initialize dataStore if it doesn't exist yet
    if (!window.dataStore) {
        window.dataStore = {
            animation: {},
            index: 0,
            active_slide: 0,
            mode: 'presentation',
            presentation:{'slides': jsonData}
        };
    } 

    

// Reference to the slide-container
let container = document.getElementById('slide-container');

render_slides(jsonData,container)


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

    
const active_id = Object.keys(window.dataStore.presentation.slides)[window.dataStore.active_slide]

//console.log(active_id)

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


function change_plotly_static(slide,staticc){

    const slideElement = document.getElementById(slide);
    

   // console.log(slideElement)
    const plotlyElements = slideElement.querySelectorAll('.PLOTLY');

    plotlyElements.forEach(element => {
        Plotly.react(element.id, element.data, element.layout, {staticPlot: staticc,responsive: true,scrollZoom: true} );   

    });

}


function apply_style(element,style) {

    //Style
    for (let styleProp in style) {
           let cssValue = style[styleProp];
           if (typeof cssValue === 'number' && ['fontSize', 'width', 'height', 'top', 'right', 'bottom', 'left'].includes(styleProp)) {
               cssValue += 'px';
           }
           //console.log(styleProp,cssValue)
	   console.log(styleProp,cssValue)
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

            add_component(key,slides[slide]['children'][key],element)
        }

        //update animation
       // window.dataStore.animation[slide] = slides[slide]['animation'] 

    }
}


function update_component(component_ID,field,value)
{

    const element = document.getElementById(component_ID)
    const className = element.className

    //Markdown
    if (className.includes('markdownComponent')){
        update_markdown(element,field,value)
    }

}

function add_component(id,data,outer_element){
   
    if (data.type === 'Markdown'){
     
        const element = document.createElement('div')
        element.className = 'markdownComponent interactable componentA'
        element.id = id
        outer_element.appendChild(element)
        update_markdown(element,'text',data.text)
        update_markdown(element,'style',data.style)
        update_markdown(element,'fontsize',data.fontsize)

    }

    if (data.type === 'Img'){
        const element = document.createElement('img');
        if (data.className) {
            element.className = 'interactable componentA';
        } else {
            element.className = data.className;
        }

        if (data.hidden){
            element.hidden=true
        }
        
        element.className ='interactable componentA'
        element.id = id
        outer_element.appendChild(element)

        const blob = new Blob([data.src], { type: 'image/png' });
        const blobURL = URL.createObjectURL(blob);

        //element.src = data.src;
        element.src = blobURL
        apply_style(element,data.style);

    }

    if (data.type === 'model3D'){

        function add_model(src){
            const element = import3DModel(new Uint8Array(src),data.style.width)
            element.id = id
            outer_element.appendChild(element)
            element.className ='interactable componentA'
            apply_style(element,data.style)
        }
        
      if (typeof data.src === 'string' && data.src.startsWith("https")) {
            fetch(data.src)
                .then(response => response.arrayBuffer()) // Handle binary data
                .then(arrayBuffer => add_model(arrayBuffer))
                .catch(error => console.error('Error fetching the model:', error));
        } else {
            add_model(data.src);
        }
    } 

    if (data.type ==='Iframe'){

        //Perhaps the external DIV is not necessary here
        const element = document.createElement('div')
       
        const iframe = document.createElement('iframe');
        iframe.width = '100%'
        iframe.height = '100%'
        iframe.setAttribute('frameborder', '1');
        iframe.src = data.src;
        element.appendChild(iframe)
        element.id = id 
        element.className ='interactable componentA'
        apply_style(element,data.style)
        outer_element.appendChild(element)
    }
  
    if (data.type ==='Plotly'){
        const config = {
            responsive: true,
            scrollZoom: true,
            staticPlot: false
            //modeBarButtonsToAdd: ["drawline","eraseshape"]
           /// displayModeBar: false
        };
        const element = document.createElement('div');
        element.id = id
        console.log(element.id)
        apply_style(element,data.style)
        //add_common_properties(element, data,true);
        //TODO: check if this is needed
        element.className = 'PartA interactable PLOTLY'
        outer_element.appendChild(element);

        //Thumbnail
        const thumbnail = document.createElement('img');
        apply_style(thumbnail,data.style)
        outer_element.appendChild(thumbnail);
        thumbnail.className = 'PartB interactable'
        thumbnail.id = id + 'THUMB'
        thumbnail.style.visibility = 'hidden'
        
        const figure = JSON.parse(data.figure)
        async function generateThumbnail(data, element, thumbnail) {
            try {
                
                const gd = await Plotly.react(element, figure.data, figure.layout, config);
                const url = await Plotly.toImage(gd);
        
                //console.log("Thumbnail URL for", data.id, ":", url);
                thumbnail.src = url;
        
            } catch (error) {
                console.error("Error while processing the graph:", error);
            }
        }
        
        // Call the function
        generateThumbnail(data, element, thumbnail);
        

    }

    if (data.type ==='Bokeh'){

        const element = document.createElement('div')
        element.id = id
        outer_element.appendChild(element)
        element.className ='interactable componentA'
        apply_style(element,data.style)

  
        async function loadBokehFromJson() {
        try {
         Bokeh.embed.embed_item(data.graph,element);
        } catch (error) {
         console.error("Error loading Bokeh plot:", error);
        }
        }
         loadBokehFromJson();

   }

   if (data.type ==='molecule'){

            // Create a new div elementelement
            const element = document.createElement("div");
            element.id = id
            outer_element.appendChild(element)
            element.className ='interactable componentA viewer_3Dmoljs'
            apply_style(element,data.style)

            
            // Initialize the viewer with a background color
            var viewer = $3Dmol.createViewer(id, {
            defaultcolors: $3Dmol.rasmolElementColors,
            backgroundColor: data.backgroundColor  
            });

            
            // Fetch the molecule and visualize it
            $3Dmol.download("pdb:" + data.structure, viewer, function() {
            viewer.setStyle({stick: {}});
            viewer.zoomTo();
            viewer.render();
           });
        }
}




// Adjusted rendering function
function render_patch(jsonData) {
   
    // Reference to the slide-container
    let container = document.getElementById('slide-container');

  
    for (const key in jsonData) {

       const patch = jsonData[key]
       if (!patch.path.split('/').includes('animation')) {
        
         
         if (patch.op === 'add'){
           //Add whole presentation 
          if (patch.path === '/slides'){render_slides(patch.value,container)}

          if (patch.path.split('/')[3] === 'children'){
           //Add component  
           const component_ID = patch.path.split('/')[4]
           const value = patch.value  
           add_component(component_ID,value,container)
           }
        }

    
        if (patch.op === 'remove'){
            //remove component
            if (patch.path.split('/')[3] === 'children'){
                const component_ID = patch.path.split('/')[4]
                document.getElementById(component_ID).remove();
            } 
        }

       if (patch.op === 'replace'){
        //[{'op': 'replace', 'path': '/slides/S0/children/S0_C0/children', 'value': 'fkk '}]
        
        const component_ID = patch.path.split('/')[4]
        const field = patch.path.split('/')[5]
        const placeholder = patch.value;
        let value = null

        if (field === 'style') {
            
            value = { [patch.path.split('/')[6]]: placeholder };
            
        }else {value = placeholder}

        
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

        
    //const active_id = 'S' + String(window.dataStore.active_slide)

    const active_id = Object.keys(window.dataStore.presentation.slides)[window.dataStore.active_slide]
    
    //console.log(active_id)

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

