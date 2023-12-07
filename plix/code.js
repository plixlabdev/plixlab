window.addEventListener('load', async function() {

//let timeout;

// Function to hide the cursor after a period of inactivity
//function handleMouseMove() {
 //   if (window.dataStore.mode === 'full') {
        // If the cursor was hidden, show it
   //     document.body.classList.remove('hide-cursor');

        // Clear any existing timeout
     //   clearTimeout(timeout);

        // Set a delay to hide the cursor again
    //    timeout = setTimeout(() => {
    //        document.body.classList.add('hide-cursor');
    //    }, 2000);  // Adjust the time as needed, currently 2 seconds
   // }
//}

// Function to hide the cursor when the mouse leaves the document
//function handleMouseOut() {
//    if (window.dataStore.mode === 'full') {
        // Clear any existing timeout when the mouse leaves the document
  //      clearTimeout(timeout);
   //     document.body.classList.add('hide-cursor');
    //}
//}

//document.addEventListener('mousemove', handleMouseMove);
//document.addEventListener('mouseout', handleMouseOut);


//For Mobile
//var hammertime = new Hammer(document.body);

//hammertime.on('swiperight', function() {
//    if (window.dataStore.mode == 'presentation') {
//        incrementSlide();
//    } else if (window.dataStore.mode == 'full') {
//        incrementEvent();
//    }
//});

//hammertime.on('swipeleft', function() {
 //   if (window.dataStore.mode == 'presentation') {
 //       decrementSlide();
 //   } else if (window.dataStore.mode == 'full') {
 //       decrementEvent();
  //  }
//});



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

   const NSlideEvents = window.dataStore.presentation['S' + String(window.dataStore.active_slide)].animation.length

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


function change_plotly_static(slide,staticc){

    const slideElement = document.getElementById(slide);

   // console.log(slideElement)
    const plotlyElements = slideElement.querySelectorAll('.PLOTLY');

    plotlyElements.forEach(element => {
        console.log(slide + '' + staticc)
        Plotly.react(element.id, element.data, element.layout, {staticPlot: staticc,responsive: true,scrollZoom: true} );   
        //element.hidden=static
        if (staticc){
        element.style.visibility='hidden'
        }
        else {element.style.visibility='visible'
           }
        


    });

}



function decrementSlide() {
    if (window.dataStore.active_slide > 0) {
        window.dataStore.active_slide -= 1;
        //window.dataStore.index = window.dataStore.animation['S' + String(window.dataStore.active_slide)].length -1 
        window.dataStore.index = window.dataStore.presentation['S' + String(window.dataStore.active_slide)].animation.length -1 


        const old_slide_id = 'S' + String(window.dataStore.active_slide+1)
        const new_slide_id = 'S' + String(window.dataStore.active_slide)
        document.getElementById(old_slide_id).style.visibility = 'hidden'

        const slide =  document.getElementById(new_slide_id)
        slide.style.visibility = 'visible'

        if (!slide.hasAttribute('tabindex')) {
            slide.setAttribute('tabindex', '-1');
        }
        slide.focus()

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
        const old_slide_id = 'S' + String(window.dataStore.active_slide-1)
        const new_slide_id = 'S' + String(window.dataStore.active_slide)

        document.getElementById(old_slide_id).style.visibility = 'hidden'

        const slide = document.getElementById(new_slide_id)
        slide.style.visibility = 'visible'


        if (!slide.hasAttribute('tabindex')) {
            slide.setAttribute('tabindex', '-1');
        }
        slide.focus()


        change_plotly_static(old_slide_id,true)
        change_plotly_static(new_slide_id,false)

        updateURL()

    }
}
   

function updateURL() {
    let currentUrl = window.location.href;
    
    // Use a regex to detect and remove the pattern #N followed by numbers
    const hashPattern = /#\d+$/;
    if (hashPattern.test(currentUrl)) {
        currentUrl = currentUrl.replace(hashPattern, '');
    }
    
    // Append the new hash fragment.
    currentUrl += "#" + String(window.dataStore.active_slide);
    
    window.history.replaceState(null, null, currentUrl);
}



function updateEventVisibility() {
    //SLIDEs use visible/hidden
    //Elements use visible/inherit
    //const arr = window.dataStore.animation['S' + String(window.dataStore.active_slide)][window.dataStore.index];
    const arr = window.dataStore.presentation.slides['S' + String(window.dataStore.active_slide)].animation[window.dataStore.index];
    for (let key in arr) {
        let element = document.getElementById(key);
        console.log(key)

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
    const containers = document.querySelectorAll('.plotly');

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

        const clickedSlideIndex = parseInt(e.target.id.substring(1));
      

        //Adapt plotly
        const old_active_slide = window.dataStore.active_slide
        if (!isNaN(clickedSlideIndex)) {
        
            window.dataStore.active_slide = clickedSlideIndex;
            updateURL()
        }

     
       switchMode()
       console.log(window.dataStore.active_slide,clickedSlideIndex)
       if (old_active_slide != clickedSlideIndex) {
         change_plotly_static('S' + String(old_active_slide),true)
         change_plotly_static('S' + String(clickedSlideIndex),false)
       }
       
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
            //console.log(el)
            el.style.pointerEvents = (window.dataStore.mode === 'grid') ? 'none' : 'auto';
        });

         // Manage PartA and PartB components
         const componentsA = document.querySelectorAll('.PartA');
         componentsA.forEach(component => {
           // component.hidden = (window.dataStore.mode === 'grid') ? true : false;
            component.style.visibility = (window.dataStore.mode === 'grid') ? 'hidden' : 'inherit';
         });
 
         const componentsB = document.querySelectorAll('.PartB');
         componentsB.forEach(component => {
            // component.hidden = (window.dataStore.mode === 'grid') ? false : true;
             component.style.visibility = (window.dataStore.mode === 'grid') ? 'inherit' : 'hidden';
         });

        

        // Adjust switch button styling
        const switchBtn = document.getElementById('switch-view-btn');
        switchBtn.className = (window.dataStore.mode === 'grid') ? 'button-base button-light' : 'button-base';

        //console.log(window.dataStore.mode)
        //Make the full-screen button disabled
        const fullscreen = document.getElementById('full-screen');
        if (window.dataStore.mode === 'grid'){
            fullscreen.style.visibility = 'hidden'
        } else {
            fullscreen.style.visibility = 'visible'
        }
        

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
        //const componentsB = document.querySelectorAll('.PartB');
        // componentsB.forEach(component => {
        // component.style.visibility = 'hidden';
        // });

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

document.getElementById('full-screen').addEventListener('click', function() {
    fullScreen();
});


});