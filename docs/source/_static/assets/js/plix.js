import { import3DModel, toggleAnimations } from './models.js';

function apply_style(element, style) {
    for (let styleProp in style) {
        let cssValue = style[styleProp];
        if (typeof cssValue === 'number' && ['fontSize', 'width', 'height', 'top', 'right', 'bottom', 'left'].includes(styleProp)) {
            cssValue += 'px';
        }
        element.style[styleProp] = cssValue;
    }
}


function update_markdown(element, field, value) {
    //Update Markdown
    // Build markdown formatter--
    const markedInstance = marked.setOptions({
        langPrefix: 'hljs language-',
        highlight: function (code, lang) {
            const language = hljs.getLanguage(lang) ? lang : 'plaintext';
            return hljs.highlight(code, { language }).value;
        }
    });

    if (field === 'text') {
        element.innerHTML = markedInstance(value);
    }

    if (field === 'style') {
        
        value['pointerEvents']= 'none'; 
        value['user-select']= "none";
        value['contenteditable']= "false" 
        value['tabindex']="-1"
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

    if (field === 'fontsize') {
        function set_fontsize(element, newFontsize) {
            let outer_element = element.parentElement;

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
        }

        set_fontsize(element, value);
    }
}


function change_plotly_static(slide, staticc) {
    const slideElement = document.getElementById(slide);
    const plotlyElements = slideElement.querySelectorAll('.PLOTLY');

    plotlyElements.forEach(element => {
        if (element.data && element.layout && element.stored_style) {
          //  apply_style(element, element.stored_style);
            element.layout.autosize = true;
            Plotly.react(element.id, element.data, element.layout, {
                staticPlot: staticc,
                responsive: true,
                scrollZoom: true
            });
        } else {
            console.warn(`Plotly data or layout is missing for element with id: ${element.id}`);
        }
    });
}

// Array to store initialization promises
let initializationPromises = [];

export function render_slide(slide_id, slide) {
    let element = document.createElement('div');
    element.className = 'slide';
    element.id = slide_id;
    element.style.backgroundColor = slide.style.backgroundColor;
    element.dataset.animation = JSON.stringify(slide.animation);
    

  

    document.getElementById('slide-container').appendChild(element);

    for (const key in slide['children']) {
        add_component(key, slide['children'][key], element);
    }
}



// Call this function during initialization


export async function render_slides(slides) {

    //Delete current slides
    const slides_to_remove = document.querySelectorAll('.slide');
    slides_to_remove.forEach(slide => slide.remove());


    for (const slide in slides) {
        render_slide(slide, slides[slide]);    
    }

    //Object.values(slides).forEach((slide, index) => {
    //    render_slide('slide_'+index, slide); 
    //});

    window.dataStore = {
        index: 0,
        active_slide: 0,
        mode: 'presentation'
    }; 
   
    await initializeCharts();
    if (window.MathJax) {
                MathJax.typesetPromise();
    }
    
  
 
}

// function update_component(component_ID, field, value) {
//     const element = document.getElementById(component_ID);
//     const className = element.className;

//     //Markdown
//     if (className.includes('markdownComponent')) {
//         update_markdown(element, field, value);
//     }
// }

function add_component(id, data, outer_element) {
    if (data.type === 'Markdown') {
        const element = document.createElement('div');
        element.className = 'markdownComponent interactable componentA';
        element.id = id;
        outer_element.appendChild(element);
        update_markdown(element, 'text', data.text);
        update_markdown(element, 'style', data.style);
        update_markdown(element, 'fontsize', data.fontsize);
    }

    if (data.type === 'Img') {
        // Create the element (assuming it's an img tag)
        const element = document.createElement('img');
        element.className = 'interactable componentA';
        element.id = id;
        outer_element.appendChild(element);

        if (typeof data.src === 'string' && data.src.startsWith("https")) {
            fetch(data.src)
                .then(response => response.arrayBuffer()) // Handle binary data
                .then(arrayBuffer => element.src = arrayBuffer)
                .catch(error => console.error('Error fetching the model:', error));
        } else {
            //local
            const arrayBuffer = data.src.data
                ? new Uint8Array(data.src.data).buffer
                : new Uint8Array(data.src).buffer;
            const blob = new Blob([arrayBuffer], { type: 'image/png' }); // Replace 'image/png' with the correct MIME type if needed
            const blobURL = URL.createObjectURL(blob);
            element.src = blobURL;
        }
        //console.log('jere')
        // Apply styles to the element
        //data.style['pointerEvents']= 'none'; 
        //data.style['user-select']= "none";
        //data.style['contenteditable']= "false" 
        //data.style['tabindex']="-1"
        apply_style(element, data.style);
    }

    if (data.type === 'model3D') {
        function add_model(src) {
            const element = import3DModel(src, data.style.width);
            element.id = id;
            outer_element.appendChild(element);
            element.className = 'interactable componentA';
            apply_style(element, data.style);
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

    if (data.type === 'Iframe') {
        const element = document.createElement('iframe');
        console.log(data)
        element.setAttribute('frameborder', '1');
        element.src = data.src;
        element.id = id;
        element.className = 'interactable componentA';
        apply_style(element, data.style);
        outer_element.appendChild(element);
    }


    if (data.type === 'Plotly') {
        const config = {
            responsive: true,
            scrollZoom: true,
            staticPlot: false
        };
        const element = document.createElement('div');
        element.id = id;
    
        apply_style(element, data.style);
        element.stored_style = data.style;
        element.className = 'PartA interactable PLOTLY';
        outer_element.appendChild(element);
    
        const figure = JSON.parse(data.figure);

        // Resize observer for Plotly charts

        const observer = new ResizeObserver(() => {Plotly.Plots.resize(element);})

        element.observer = observer;

        const style = element.stored_style;
        if (style) {
          element.style.width = style.width || '100%';
          element.style.height = style.height || '100%';
        }
        Plotly.react(element, figure.data, figure.layout, config);
        Plotly.Plots.resize(element); // Ensure proper resizing
                
            
    
        // Initialize the Plotly chart
    
    
        // Optional: Handle thumbnails or other features

        const thumbnail = document.createElement('img');
        apply_style(thumbnail, data.style);
        outer_element.appendChild(thumbnail);
        thumbnail.className = 'PartB interactable';
        thumbnail.id = id + 'THUMB';
        thumbnail.style.visibility = 'hidden';
    
        async function generateThumbnail(data, element, thumbnail) {
        try {
                const gd = await Plotly.react(element, figure.data, figure.layout, config);
                const url = await Plotly.toImage(gd);
                thumbnail.src = url;
            } catch (error) {
                console.error("Error while processing the graph:", error);
            }
        }
    
        const initializationPromise = generateThumbnail(data, element, thumbnail);
        initializationPromises.push(initializationPromise);
    }

    if (data.type === 'Bokeh') {
        const element = document.createElement('div');
        element.id = id;
        outer_element.appendChild(element);
        element.className = 'interactable componentA';
        apply_style(element, data.style);

        async function loadBokehFromJson() {
            try {
                Bokeh.embed.embed_item(data.graph, element);
            } catch (error) {
                console.error("Error loading Bokeh plot:", error);
            }
        }
        loadBokehFromJson();
    }

    if (data.type === 'molecule') {
        // Create a new div element
        const element = document.createElement("div");
        id = 'test';
        element.id = id;
        outer_element.appendChild(element);
        //element.className ='interactable componentA viewer_3Dmoljs'
        //element.setAttribute('data-pdb',data.structure);
        //element.setAttribute('data-backgroundcolor','0xffffff');
        //element.setAttribute('data-style','stick');
        //element.setAttribute('data-ui','true');
        apply_style(element, data.style);

        // Initialize the viewer with a background color
        var viewer = $3Dmol.createViewer('test', {
            defaultcolors: $3Dmol.rasmolElementColors,
            backgroundColor: data.backgroundColor
        });

        $3Dmol.download("pdb:" + data.structure, viewer, function () {
            viewer.setStyle({ stick: {} });
            viewer.zoomTo();
            viewer.render();
        });
    }
}

// // Adjusted rendering function
// export async function render_patch(jsonData) {
//     // Clear initializationPromises
//     initializationPromises = [];

//     // Reference to the slide-container
//     let container = document.getElementById('slide-container');

//     for (const key in jsonData) {
//         const patch = jsonData[key];
//         // const operation = patch.op
//         // console.log('Operation ',operation)
//         // console.log(patch.patch)

//         if (!patch.path.split('/').includes('animation')) {
//             if (patch.op === 'add') {
//                 //Add whole presentation 
//                 if (patch.path === '/slides') {
//                     await render_slides(patch.value);
//                 }

//                 if (patch.path.split('/')[3] === 'children') {
//                     //Add component  
//                     const component_ID = patch.path.split('/')[4];
//                     const value = patch.value;
//                     add_component(component_ID, value, container);
//                 }
//             }

//             if (patch.op === 'remove') {
//                 //remove component
//                 if (patch.path.split('/')[3] === 'children') {
//                     const component_ID = patch.path.split('/')[4];
//                     document.getElementById(component_ID).remove();
//                 } 
//             }

//             if (patch.op === 'replace') {
//                 const component_ID = patch.path.split('/')[4];
//                 const field = patch.path.split('/')[5];
//                 const placeholder = patch.value;
//                 let value = null;

//                 if (field === 'style') {
//                     value = { [patch.path.split('/')[6]]: placeholder };
//                 } else {
//                     value = placeholder;
//                 }

//                 update_component(component_ID, field, value);
//             }
//         }
//     }

//     // Run MathJax
//     if (window.MathJax) {
//         MathJax.typesetPromise();
//     }

//     // Initialize charts after rendering
//     await initializeCharts();
// }

async function initializeCharts() {

    if (initializationPromises.length > 0) {
        await Promise.all(initializationPromises);
    }
    //console.log(window.dataStore.active_slide)
 

   //console.log('slides') 
    //console.log(window.dataStore.presentation.slides)

    // Update visibility
    const slides = document.querySelectorAll(".slide");

     
    //slides.forEach((slide, index) => {
    //     if (window.dataStore.mode === 'presentation' && index !== window.dataStore.active_slide) {
    //         slide.style.visibility = 'hidden';
    //     } else {
    //         slide.style.visibility = 'visible';
    //     }
    // });


//    const active_id = Object.keys(window.dataStore.presentation.slides)[window.dataStore.active_slide];
//     for (let i = 0; i < slides.length; i++) {
//         if (slides[i].id === active_id) {
//             change_plotly_static(slides[i].id, false);
//             slides[i].style.visibility = 'visible';
//         } else {
//             change_plotly_static(slides[i].id, true);
//             slides[i].style.visibility = 'hidden';
//         }
//     }

    for (let i = 0; i < slides.length; i++) {
        if (i==0) {
            change_plotly_static(slides[i].id, false);
            slides[i].style.visibility = 'visible';
        } else {
            change_plotly_static(slides[i].id, true);
            slides[i].style.visibility = 'hidden';
        }
    }




}



window.addEventListener('load', async function () {



    document.addEventListener('keydown', function (event) {
      
        if (window.dataStore.mode == 'presentation') {
            if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
                
                incrementSlide();
            } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
                decrementSlide();
            }
        }

        if (window.dataStore.mode == 'full') {
            if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
                incrementEvent();
            } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
                decrementEvent();
            }
        }
    });

    document.getElementById('aleft').addEventListener('click', function (event) {
        if (window.dataStore.mode == 'presentation') {
            decrementSlide();
        }
    });

    document.getElementById('aright').addEventListener('click', function (event) {
        if (window.dataStore.mode == 'presentation') {
            incrementSlide();
        }
    });

    function incrementEvent() {

        //const totalSlides = document.querySelectorAll(".slide").length;
        //const slide_ids = Object.keys(window.dataStore.presentation.slides);
        //const NSlideEvents = window.dataStore.presentation.slides[slide_ids[window.dataStore.active_slide]].animation.length;
        const NSlideEvents = JSON.parse(document.querySelectorAll(".slide")[window.dataStore.active_slide].dataset.animation).length;

        console.log(document.querySelectorAll(".slide")[window.dataStore.active_slide].dataset.animation)
        if (window.dataStore.index < NSlideEvents - 1) {
            window.dataStore.index += 1;
        } else {
            incrementSlide();
        }

        updateEventVisibility();
    }

    function decrementEvent() {
        if (window.dataStore.index > 0) {
            window.dataStore.index -= 1;
        } else {
            decrementSlide();
        }

        updateEventVisibility();
    }

    function decrementSlide() {
        const slides = document.querySelectorAll(".slide"); // Select all slides
        const totalSlides = slides.length;
    
        // Check if there is a previous slide to show
        if (window.dataStore.active_slide > 0) {
            // Get the current slide and hide it
            const currentSlide = slides[window.dataStore.active_slide];
            currentSlide.style.visibility = 'hidden'; // Use 'hidden' to hide it
    
            // Get the previous slide and show it
            const prevSlide = slides[window.dataStore.active_slide - 1];
            prevSlide.style.visibility = 'visible';
    
            // Update the dataStore
            window.dataStore.active_slide -= 1;
            window.dataStore.index = 0;
    
            // Trigger plot updates
            change_plotly_static(currentSlide.id, true);
            change_plotly_static(prevSlide.id, false);
        }
    }
    

    function incrementSlide() {
        const slides = document.querySelectorAll(".slide"); // Select all slides
        const totalSlides = slides.length;
        //console.log('increment slide')
    
        // Check if there are more slides to show
        if (window.dataStore.active_slide < totalSlides - 1) {
            // Get the current slide and hide it
            const currentSlide = slides[window.dataStore.active_slide];
            currentSlide.style.visibility = 'hidden'; // Use 'hidden' for visibility
    
            // Get the next slide and show it
            const newSlide = slides[window.dataStore.active_slide + 1];
            newSlide.style.visibility = 'visible';
    
            // Update the dataStore
            window.dataStore.active_slide += 1;
            window.dataStore.index = 0;
    
            // Trigger plot updates
            change_plotly_static(currentSlide.id, true);
            change_plotly_static(newSlide.id, false);
        }
    }
    
        

    function updateURL() {
        // Update URL if necessary
    }

    function updateEventVisibility() {
       
        const slide = document.querySelectorAll(".slide")[window.dataStore.active_slide]

        const animation = JSON.parse(slide.dataset.animation)[window.dataStore.index];

    
        for (let key in animation) {
           
            let element = document.getElementById(slide.id + '_' + key);
           
            if (animation[key]) {
                element.style.visibility = 'hidden';

                if (element.className === 'PLOTLY') {
                    element.hidden = true;
                }
            } else {
                element.style.visibility = 'inherit';
                if (element.className === 'PLOTLY') {
                    element.hidden = false;
                }
            }
        }
    }

    function updatePlotly() {
        const containers = document.querySelectorAll('.PLOTLY');

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
            if (window.dataStore.mode === 'grid') {

                const clickedSlideIndex = e.target.id;

                //const slides_ids = Object.keys(window.dataStore.presentation.slides);

                const slides_ids = Array.from(document.querySelectorAll(".slide"), slide => slide.id);

                const old_active_slide = window.dataStore.active_slide;

                window.dataStore.active_slide = slides_ids.indexOf(clickedSlideIndex);

                //updateURL();

                switchMode();

                change_plotly_static(slides_ids[old_active_slide], true); //old
                change_plotly_static(clickedSlideIndex, false); //new
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
            if (window.dataStore.mode === 'presentation' && index !== window.dataStore.active_slide) {
                slide.style.visibility = 'hidden';
            } else {
                slide.style.visibility = 'visible';
            }
        });

        //Make the interactive plot disappear
        updatePlotly();

        //Change the number of rows in grid
        function setGridRowsBasedOnN(N) {
            const numberOfRows = Math.ceil(N / 4);
            const gridElement = document.querySelector('.grid');
            gridElement.style.gridTemplateRows = `repeat(${numberOfRows}, 25%)`;
        }

        if (window.dataStore.mode === 'grid') {
            const N = document.querySelectorAll(".slide").length;
            setGridRowsBasedOnN(N);
        }

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

        const aleft = document.getElementById('aleft');
        aleft.style.visibility = (window.dataStore.mode === 'grid') ? 'hidden' : 'visible';

        const aright = document.getElementById('aright');
        aright.style.visibility = (window.dataStore.mode === 'grid') ? 'hidden' : 'visible';

        //Adjust model animation
        toggleAnimations(window.dataStore.mode !== 'grid');
    }

    document.getElementById('switch-view-btn').addEventListener('click', function () {
        switchMode();
    });

    function fullScreen() {
        var outerContainer = document.getElementById('slide-container');

        function adjustFontSize() {
            outerContainer.classList.add('fullscreen-mode');
            window.dataStore.mode = 'full';
            window.dataStore.index = 0;

            updateEventVisibility();
        }

        outerContainer.requestFullscreen().then(adjustFontSize);

        document.onfullscreenchange = function () {
            if (!document.fullscreenElement) {
                outerContainer.classList.remove('fullscreen-mode');
                window.dataStore.mode = 'presentation';

                // Show the active slide
                const slides = document.querySelectorAll(".slide");
                slides.forEach((slide, index) => {
                    slide.style.visibility = (index == window.dataStore.active_slide) ? 'visible' : 'hidden';
                });

                // Show all components in presentation mode
                const components = document.querySelectorAll(".componentA");
                components.forEach((component, index) => {
                    component.style.visibility = 'inherit';
                });
            }
        }
    }

    // Uncomment if you have a full-screen button
     document.getElementById('full-screen').addEventListener('click', function() {
        fullScreen();
     });
});
