import {import3DModel,toggleAnimations} from './models.js';

    

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

function resize_plotly_chart(element) {
    Plotly.Plots.resize(element);
}

function change_plotly_static(slide, staticc) {
    const slideElement = document.getElementById(slide);
    const plotlyElements = slideElement.querySelectorAll('.PLOTLY');

    plotlyElements.forEach(element => {
        Plotly.react(element.id, element.data, element.layout, {
            staticPlot: staticc,
            responsive: true,
            scrollZoom: true
        });
        resize_plotly_chart(element);
    });
}

 export function render_slide(slide_id,slide)
 {
     
     let element = document.createElement('div');
     element.className = 'slide';
     element.id = slide_id
     element.style.backgroundColor = slide.style.backgroundColor

     document.getElementById('slide-container').appendChild(element)
        
     for (const key in slide['children']){
            add_component(key,slide['children'][key],element)
     }

    
 }



function render_slides(slides){

    
    for (const slide in slides) {

        render_slide(slide,slides[slide])

        //create slide
       // let element = document.createElement('div');
       // element.className = 'slide';
       // element.id = slide
       // element.style.backgroundColor = slides[slide].style.backgroundColor
       // container.appendChild(element)
        //------
        
        //render elements--
       // for (const key in slides[slide]['children']){

       //     add_component(key,slides[slide]['children'][key],element)
       // }

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
       
      
        
       function isValidURL(str) {
        try {
            new URL(str);
            return true;
        } catch (_) {
            return false;
        }
    }
    
      // Create the element (assuming it's an img tag)
      const element = document.createElement('img');
      element.className = 'interactable componentA';
      element.id = id;
      outer_element.appendChild(element);
      
      //The issue is that for local use it is not a valid URL

      // Check if data.src is a valid URL or binary data
      if (typeof data.src === 'string' && isValidURL(data.src)) {
        // data.src is already a valid URL, use it directly
        element.src = data.src;
      } else {
        // data.src is likely binary data, create a Blob
        const blob = new Blob([data.src], { type: 'image/png' });
        const blobURL = URL.createObjectURL(blob);
        console.log(blobURL);  // Debug the created blob URL
    
        // Set the Blob URL as the image source
        element.src = blobURL;
      }
    
    // Apply styles to the element
    apply_style(element, data.style);

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


        const element = document.createElement('iframe');  // Directly create the iframe
        element.setAttribute('frameborder', '1');  // Set the frameborder to 1
        element.src = data.url;  // Set the iframe's source URL
        element.id = id;  // Set a unique ID for the iframe
        element.className = 'interactable componentA';  // Apply classes for styling
        apply_style(element, data.style);  // Apply additional styles through your custom apply_style function
        outer_element.appendChild(element); 
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
       
        apply_style(element,data.style)
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
        //const gd = Plotly.react(element, figure.data, figure.layout, config);
        //const url    = Plotly.toImage(gd);
        //thumbnail.src = url;
              //console.log("Thumbnail URL for", data.id, ":", url);
          
      
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
            ///TODO: Shorten the ID (eliminate the uid)
            
            // Create a new div elementelement
            const element = document.createElement("div");
            id = 'test'
            element.id = id
            outer_element.appendChild(element)
            //element.className ='interactable componentA viewer_3Dmoljs'
            //element.setAttribute('data-pdb',data.structure);
            //element.setAttribute('data-backgroundcolor','0xffffff');
            //element.setAttribute('data-style','stick');
            //element.setAttribute('data-ui','true');
            apply_style(element,data.style)

            // Initialize the viewer with a background color
            var viewer = $3Dmol.createViewer('test', {
            defaultcolors: $3Dmol.rasmolElementColors,
            backgroundColor: data.backgroundColor  
            });
  
    
            $3Dmol.download("pdb:" + data.structure, viewer, function() {
            viewer.setStyle({stick: {}});
            viewer.zoomTo();
            viewer.render();
            })

        
        }
}




// Adjusted rendering function
export function render_patch(jsonData) {
   
    // Reference to the slide-container
    let container = document.getElementById('slide-container');

  
    for (const key in jsonData) {

       const patch = jsonData[key]
       if (!patch.path.split('/').includes('animation')) {
        
         
         if (patch.op === 'add'){
           //Add whole presentation 
          if (patch.path === '/slides'){render_slides(patch.value)}

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
    //const currentUrl = window.location.href
   // if (currentUrl.charAt(currentUrl.length - 2) !== '#' &&
   // currentUrl.charAt(currentUrl.length - 3) !== '#' &&
   // currentUrl.charAt(currentUrl.length - 4) !== '#')  {
   //  window.location.href += "#" + String(window.dataStore.active_slide);
   // } else {
    //    let parts = currentUrl.split('#');
     //   let number = parseInt(parts[1], 10);
     //   window.dataStore.active_slide =number;}

        

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

window.addEventListener('load', async function() {


    document.addEventListener('keydown', function(event) {
       
        if (window.dataStore.mode == 'presentation') {
            if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
                incrementSlide();
            } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
                decrementSlide() ;
            }
        }
    
        if (window.dataStore.mode == 'full') {
         if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
            incrementEvent();
         } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
            decrementEvent() ;
         }
        }
    
      })
    
    
    document.getElementById('aleft').addEventListener('click', function(event) {
        if (window.dataStore.mode == 'presentation') {
            decrementSlide();
        }
    });
    
    document.getElementById('aright').addEventListener('click', function(event) {
        if (window.dataStore.mode == 'presentation') {
            incrementSlide();
        }
    }); 
    
    
    
    
    function incrementEvent() {    
    
    
       const totalSlides = document.querySelectorAll(".slide").length;
       //const NSlideEvents = window.dataStore.animation['S' + String(window.dataStore.active_slide)].length
       //const NSlideEvents = window.dataStore.presentation.slides['S' + String(window.dataStore.active_slide)].animation.length
    
    
       const slide_ids = Object.keys(window.dataStore.presentation.slides)
       const NSlideEvents = window.dataStore.presentation.slides[slide_ids[window.dataStore.active_slide]].animation.length
    
    
       if (window.dataStore.index < NSlideEvents - 1){
          window.dataStore.index += 1; 
        } else { incrementSlide()}
          
        updateEventVisibility()
    }
    
    
    function decrementEvent() {    
    
    
       if (window.dataStore.index > 0){
          window.dataStore.index -= 1;    
       } else { decrementSlide()}
    
        updateEventVisibility()
    
    }
    
    
    
    function decrementSlide() {
        if (window.dataStore.active_slide > 0) {
            window.dataStore.active_slide -= 1;
    
    
    
            const slide_ids = Object.keys(window.dataStore.presentation.slides)
            window.dataStore.index = window.dataStore.presentation.slides[slide_ids[window.dataStore.active_slide]].animation.length -1
            const old_slide_id = slide_ids[window.dataStore.active_slide+1]
            const new_slide_id = slide_ids[window.dataStore.active_slide]
    
    
            document.getElementById(old_slide_id).style.visibility = 'hidden'
    
            const slide =  document.getElementById(new_slide_id)
            slide.style.visibility = 'visible'
    
    
            change_plotly_static(old_slide_id,true)
            change_plotly_static(new_slide_id,false)
    
            updateURL()
          
        }
    
    }
    
    
    
    function incrementSlide() {
        const totalSlides = document.querySelectorAll(".slide").length;
         if (window.dataStore.active_slide < totalSlides - 1) {
            window.dataStore.active_slide += 1
            window.dataStore.index = 0
    
    
            const slide_ids = Object.keys(window.dataStore.presentation.slides)
            
            const old_slide_id = slide_ids[window.dataStore.active_slide-1]
            const new_slide_id = slide_ids[window.dataStore.active_slide]
    
    
    
            document.getElementById(old_slide_id).style.visibility = 'hidden'
    
            const slide = document.getElementById(new_slide_id)
            slide.style.visibility = 'visible'
    
    
            change_plotly_static(old_slide_id,true)
            change_plotly_static(new_slide_id,false)
    
            updateURL()
    
        }
    }
       
    
    function updateURL() {
    //    let currentUrl = window.location.href;
        
        // Use a regex to detect and remove the pattern #N followed by numbers
    //    const hashPattern = /#\d+$/;
    //    if (hashPattern.test(currentUrl)) {
    //        currentUrl = currentUrl.replace(hashPattern, '');
    //    }
        
        // Append the new hash fragment.
    //    currentUrl += "#" + String(window.dataStore.active_slide);
        
     //   window.history.replaceState(null, null, currentUrl);
    }
    
    
    
    function updateEventVisibility() {
        //SLIDEs use visible/hidden
        //Elements use visible/inherit
       
    
        const slide_id = Object.keys(window.dataStore.presentation.slides)[window.dataStore.active_slide]
        const arr = window.dataStore.presentation.slides[slide_id].animation[window.dataStore.index];
    
        for (let key in arr) {
            let element = document.getElementById(slide_id + '_' + key);
            
    
            if (arr[key]) {
                element.style.visibility = 'hidden';
                
                if (element.className === 'PLOTLY'){
                     element.hidden=true
                }
            } else {
                element.style.visibility = 'inherit';
                if (element.className === 'PLOTLY'){
                    element.hidden=false
               }
            }
        } 
    }
    
    
    
    
    function updatePlotly(){
    
        //TODO: We need to avoid rerendering this. 
        const containers = document.querySelectorAll('.PLOTLY');
    
        // Loop through each container
        containers.forEach(container => {
        if (window.dataStore.mode === 'grid') {
          container.hidden = true;
       } else {
         container.hidden = false;
       }
       });
    }
    
    
    document.body.addEventListener('click', e => {
        
        if (e.target.classList.contains('slide')) {
    
            if (window.dataStore.mode === 'grid'){
    
            const clickedSlideIndex = e.target.id;
            const slides_ids = Object.keys(window.dataStore.presentation.slides)
            
          
            const old_active_slide = window.dataStore.active_slide
            
            window.dataStore.active_slide = slides_ids.indexOf(clickedSlideIndex); 
    
           
            updateURL()
    
    
            switchMode()
         
        
            change_plotly_static(slides_ids[old_active_slide],true) //old
            change_plotly_static(clickedSlideIndex,false) //new
            
            
    
           
           
        }
    }
    });
    
    
    
    function switchMode() {
            //change mode
            window.dataStore.mode = (window.dataStore.mode === 'grid') ? 'presentation' : 'grid';
            document.getElementById('slide-container').className = window.dataStore.mode;
    
    
            // Hide/Show slides
            const slides = document.querySelectorAll(".slide");
    
           
            slides.forEach((slide, index) => {
            if (window.dataStore.mode === 'presentation' && index !== window.dataStore.active_slide){
               
                slide.style.visibility = 'hidden'
            } else {
              
                slide.style.visibility = 'visible'
            }
    
            });
           
             //Make the interactive plot disappear
            updatePlotly()
            //Change the number of rows in grid--------
            function setGridRowsBasedOnN(N) {
              const numberOfRows = Math.ceil(N / 4);
               const gridElement = document.querySelector('.grid');
               gridElement.style.gridTemplateRows = `repeat(${numberOfRows}, 25%)`;
    
               }
    
            if (window.dataStore.mode === 'grid'){  
             const N = document.querySelectorAll(".slide").length
             setGridRowsBasedOnN(N);}
            //----------------------------------------
    
            // Manage interactable elements
            const interactables = document.querySelectorAll('.interactable');
            interactables.forEach(el => {
                el.style.pointerEvents = (window.dataStore.mode === 'grid') ? 'none' : 'auto';
            });
    
             // Manage PartA and PartB components
             const componentsA = document.querySelectorAll('.PartA');
             componentsA.forEach(component => {
            component.style.visibility = (window.dataStore.mode === 'grid') ? 'hidden' : 'inherit';
             });
     
             const componentsB = document.querySelectorAll('.PartB');
             componentsB.forEach(component => {
                 component.style.visibility = (window.dataStore.mode === 'grid') ? 'inherit' : 'hidden';
             });
    
            
    
            // Adjust switch button styling
            const switchBtn = document.getElementById('switch-view-btn');
            switchBtn.className = (window.dataStore.mode === 'grid') ? 'button-base button-light' : 'button-base';
    
            //console.log(window.dataStore.mode)
            //Make the full-screen button disabled
            //const fullscreen = document.getElementById('full-screen');
            //if (window.dataStore.mode === 'grid'){
            //    fullscreen.style.visibility = 'hidden'
            //} else {
            //    fullscreen.style.visibility = 'visible'
           // }
            
    
            const aleft = document.getElementById('aleft');
            if (window.dataStore.mode === 'grid'){
                aleft.style.visibility = 'hidden'
            } else {
    
                aleft.style.visibility = 'visible'
            }
            const aright = document.getElementById('aright');
            if (window.dataStore.mode === 'grid'){
                aright.style.visibility = 'hidden'
            } else {
                aright.style.visibility = 'visible'
            }
    
            //Adjust model animation
            if (window.dataStore.mode === 'grid'){
               toggleAnimations(false);
            }
            else { toggleAnimations(true)}   
    
    }
    
    
    document.getElementById('switch-view-btn').addEventListener('click', function() {
            switchMode();
    });
    
       
    function fullScreen() {
    
        var outerContainer = document.getElementById('slide-container');
    
        function adjustFontSize() {
            outerContainer.classList.add('fullscreen-mode');
            window.dataStore.mode = 'full';
            window.dataStore.index = 0;
           
            updateEventVisibility()
          
        }
        
        outerContainer.requestFullscreen().then(adjustFontSize);
        
    
          document.onfullscreenchange = function() {
               if (!document.fullscreenElement) {
    
                    outerContainer.classList.remove('fullscreen-mode');
                  
                        window.dataStore.mode = 'presentation';
    
                        // Show the active slide
                        const slides = document.querySelectorAll(".slide");
                        slides.forEach((slide, index) => {
    
                        if (index == window.dataStore.active_slide){
    
                            slide.style.visibility = 'visible'
                        } else {
                            slide.style.visibility = 'hidden'}                
                        })
    
                       
                        //show all components in presentation mode
                        const components = document.querySelectorAll(".componentA");
                        components.forEach((component, index) => {
                        component.style.visibility = 'inherit'
                        //component.hidden = false;
                         });
        
                    };
            
            }
    
        
    
    }
    
    
    //document.getElementById('full-screen').addEventListener('click', function() {
    //    fullScreen();
    //});
    
    
    });
    
    //Save presentation for self-deployment
    function savePresentation() {
        var element = document.documentElement;
        if (!element) {
            console.error('Document element not found.');
            return; // Exit the function if the element is not found
        }
        
        // Serialize the data stored in window.dataStore to a JSON string
        var dataStoreJson = JSON.stringify(window.dataStore || {});
        
        // Create a script tag that will re-initialize window.dataStore with the saved data
        var dataStoreScript = `<script>window.dataStore = ${dataStoreJson};</script>`;
        
        // Capture the entire HTML content
        var htmlContent = element.outerHTML;
        
        // Use a regular expression to remove the specific <script> tag from the HTML content
        // This pattern matches the <script> tag with variations in attribute order, additional attributes, and whitespace
        //var scriptPattern = /<script\s+type=['"]module['"]\s+src=['"]assets\/js\/load\.js['"]\s*><\/script>/g;
        //var modifiedHtmlContent = htmlContent.replace(scriptPattern, '');
        
        // Append the dataStore script to the modified HTML content
        var modifiedHtmlContent = htmlContent.replace('</body>', dataStoreScript + '</body>');
        
        // Debugging: Log the final HTML to ensure it's correct
        //("Final HTML content:", modifiedHtmlContent);
    
        // Create a Blob with the final HTML content
        var blob = new Blob([modifiedHtmlContent], { type: 'text/html' });
        
        // Create and trigger a download link
        var downloadLink = document.createElement('a');
        downloadLink.href = window.URL.createObjectURL(blob);
        downloadLink.download = 'presentation.html'; // Name of the file to download
        document.body.appendChild(downloadLink);
        downloadLink.click(); // Trigger the download
        document.body.removeChild(downloadLink); // Clean up
    }
    
    // Assuming 'download_html' is the ID of the button that triggers the download
    //document.getElementById('download_html').addEventListener('click', function() {
    //    savePresentation();
    //});
