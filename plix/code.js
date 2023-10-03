//document.addEventListener('DOMContentLoaded', function() {
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


function incrementEvent() {    

    //const totalEvents = window.dataStore.animation.length;
    //if (window.dataStore.index < totalEvents - 1) {
    //   window.dataStore.index += 1;
    //   updateEventVisibility()
   // }

   const totalSlides = document.querySelectorAll(".slide").length;
   const NSlideEvents = window.dataStore.animation['S' + String(window.dataStore.active_slide)].length
   //console.log(window.dataStore.index,NSlideEvents,window.dataStore.active_slide, totalSlides)
   if (window.dataStore.index < NSlideEvents - 1){
      window.dataStore.index += 1; 
    } else {
        if (window.dataStore.active_slide < totalSlides - 1){
            document.getElementById('S' + String( window.dataStore.active_slide)).hidden=true
            window.dataStore.index = 0
            window.dataStore.active_slide +=1}
            document.getElementById('S' + String( window.dataStore.active_slide)).hidden=false
    }

    updateEventVisibility()
}


function decrementEvent() {    

   //if (window.dataStore.index > 0) {
   //     window.dataStore.index -= 1;
   //     updateEventVisibility()
   // }

   console.log(window.dataStore.index,window.dataStore.active_slide)
   if (window.dataStore.index > 0){
      window.dataStore.index -= 1; 
      
    } else {
   if (window.dataStore.active_slide >0){
            
            console.log(window.dataStore.index,window.dataStore.active_slide)
            document.getElementById('S' + String( window.dataStore.active_slide)).hidden=true
            window.dataStore.active_slide -=1
            document.getElementById('S' + String( window.dataStore.active_slide)).hidden=false
            window.dataStore.index = window.dataStore.animation['S' + String(window.dataStore.active_slide)].length -1 
   }
  }

    updateEventVisibility()

}



function incrementSlide() {
    const totalSlides = document.querySelectorAll(".slide").length;
     if (window.dataStore.active_slide < totalSlides - 1) {
        window.dataStore.active_slide += 1;

        //Change visibility
        document.getElementById('S' + String(window.dataStore.active_slide-1)).hidden = true
        document.getElementById('S' + String(window.dataStore.active_slide)).hidden = false
    }
}
   


function decrementSlide() {
    if (window.dataStore.active_slide > 0) {
        window.dataStore.active_slide -= 1;
         //Change visibility
         document.getElementById('S' + String(window.dataStore.active_slide+1)).hidden = true
         document.getElementById('S' + String(window.dataStore.active_slide)).hidden = false
    }

}



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





function updateEventVisibility() {

    arr = window.dataStore.animation['S' + String(window.dataStore.active_slide)][window.dataStore.index]

    //arr =  window.dataStore.animation[ window.dataStore.index]
    for (let key in arr) {
        //console.log(key)
        document.getElementById(key).hidden = arr[key]
    } 

}


//function updateSlidesVisibility() {
 //   try {
 //       var slides = document.querySelectorAll(".slide");
        
 //       slides.forEach(function(slide, index) {
  //          if (!slide) {
  //              console.error('Slide at index:', index, 'not found!');
  //              return;
  //          }
          
            // Using the index directly for comparison with active_slide
  //          if (window.dataStore.mode === 'presentation' && index !== window.dataStore.active_slide) {
  //              slide.hidden = true;
  //          } else {
  //              slide.hidden = false;
  //          }
  //      });
  //  } catch (error) {
   //     console.error('Error updating visibility for slides', error);
   // }
//}

document.body.addEventListener('click', e => {
    const ratio = 0.24;
    if (e.target.classList.contains('slide')) {
        const clickedSlideIndex = parseInt(e.target.getAttribute('data-index'));
        if (!isNaN(clickedSlideIndex)) {
            //window.dataStore.active_slide = clickedSlideIndex;
            
            window.dataStore.active_slide = clickedSlideIndex;
            //console.log(window.dataStore.active_slide);
        }

       if (window.dataStore.mode === 'grid')
       {
        window.dataStore.mode = 'presentation'
        document.getElementById('slide-container').className = window.dataStore.mode;

        // Scale text
        const textElements = document.querySelectorAll('.markdownComponent');
        textElements.forEach((textElement) => {
        const fontSizePx = parseFloat(window.getComputedStyle(textElement).fontSize);
        const newFontSize = (window.dataStore.mode === 'grid') ? fontSizePx * ratio : fontSizePx / ratio;
        textElement.style.fontSize = `${newFontSize}px`;
       });

       // Hide/Show slides
      const slides = document.querySelectorAll(".slide");
     
       slides.forEach((slide, index) => {
      
       slide.hidden = (window.dataStore.mode === 'presentation' && index !== window.dataStore.active_slide);
       });

         

        // Manage interactable elements
        const interactables = document.querySelectorAll('.interactable');
        //console.log(interactables.length)
        interactables.forEach(el => {
            el.style.pointerEvents = (window.dataStore.mode === 'grid') ? 'none' : 'auto';
        });

         // Manage PartA and PartB components
         const componentsA = document.querySelectorAll('.PartA');
         componentsA.forEach(component => {
             component.hidden = (window.dataStore.mode === 'grid') ? true : false;
         });
 
         const componentsB = document.querySelectorAll('.PartB');
         componentsB.forEach(component => {
             component.hidden = (window.dataStore.mode === 'grid') ? false : true;
         });

         //Make the full-screen button disabled
         const fullscreen = document.getElementById('full-screen');
         fullscreen.style.visibility = 'visible'
         
       }
        
    }
});

function switchMode() {
        const ratio = 0.24;
        //change mode
        window.dataStore.mode = (window.dataStore.mode === 'grid') ? 'presentation' : 'grid';
        document.getElementById('slide-container').className = window.dataStore.mode;


        // Scale text
        const textElements = document.querySelectorAll('.markdownComponent');
        textElements.forEach((textElement) => {
            const fontSizePx = parseFloat(window.getComputedStyle(textElement).fontSize);
            const newFontSize = (window.dataStore.mode === 'grid') ? fontSizePx * ratio : fontSizePx / ratio;
            textElement.style.fontSize = `${newFontSize}px`;
            //function updateSlidesVisibility() {
            //component.hidden = (window.dataStore.mode === 'grid') ? false : true;}
        });

        // Hide/Show slides
        const slides = document.querySelectorAll(".slide");
        slides.forEach((slide, index) => {
        slide.hidden = (window.dataStore.mode === 'presentation' && index !== window.dataStore.active_slide);
        });

        // Show all components when going to grid mode
        //const components = document.querySelectorAll(".component");
        //components.forEach((component, index) => {
        //component.hidden = (window.dataStore.mode === 'presentation');
        //});

        //Update visibility
        //if (window.dataStore.mode === 'grid') {
        //    const components = document.querySelectorAll(".component");
        //    components.forEach((component, index) => {
        //    component.hidden = false})
        //} else {
        //     updateSlidesVisibility() 
       // }
        
        //console.log( window.dataStore.active_slide)
        // Adjust switch button styling
        const switchBtn = document.getElementById('switch-view-btn');
        switchBtn.className = (window.dataStore.mode === 'grid') ? 'button-base button-light' : 'button-base';


        // Manage interactable elements
        const interactables = document.querySelectorAll('.interactable');
        //console.log(interactables.length)
        interactables.forEach(el => {
            el.style.pointerEvents = (window.dataStore.mode === 'grid') ? 'none' : 'auto';
        });

        //console.log(window.dataStore.mode)
        //Make the full-screen button disabled
        const fullscreen = document.getElementById('full-screen');
        if (window.dataStore.mode === 'grid'){
            fullscreen.style.visibility = 'hidden'
        } else {
            fullscreen.style.visibility = 'visible'
        }

    }


document.getElementById('switch-view-btn').addEventListener('click', function() {
        switchMode();
});

   
function fullScreen() {

    var outerContainer = document.getElementById('outer-container');
    //console.log(outerContainer.offoriginalOuterContainer.offsetWidthsetWidth,outerContainer.offsetHeight)
    originalWidth = outerContainer.offsetWidth
    // Store original font sizes as percentages of slideArea's width
    const textElements = document.querySelectorAll('.markdownComponent');
    const originalFontSizes = [];
    textElements.forEach((textElement) => {
    const fontSizePx = parseInt(window.getComputedStyle(textElement).fontSize);
    const fontSizePercentage = fontSizePx / originalWidth;
    originalFontSizes.push(fontSizePercentage);
     });
    //-------------------------------------------------------------------

    function adjustFontSize() {
            const slideAreaWidth = outerContainer.offsetWidth;
            textElements.forEach((textElement, i) => {
            const fontSize = slideAreaWidth * originalFontSizes[i];
            textElement.style.fontSize = fontSize + 'px';
            //console.log('Forward Full before '  +  originalWidth + ' ' + originalFontSizes[i]*originalWidth + 'px, after ' +fontSize  + 'px');
            outerContainer.classList.add('fullscreen-mode');
            window.dataStore.mode = 'full';
            //Go into Presenting mode (Full)
            //Reset index (which belong to one slide)
            window.dataStore.index = 0
            updateEventVisibility()
        });}

      document.onfullscreenchange = function() {
            if (!document.fullscreenElement) {
                textElements.forEach((textElement, i) => {
                    const fontSize = outerContainer.offsetWidth * originalFontSizes[i];
                    textElement.style.fontSize = fontSize + 'px';
                    window.dataStore.mode = 'presentation';
                    console.log(window.dataStore.mode)
                    outerContainer.classList.remove('fullscreen-mode');

                    // Show the active slide
                    const slides = document.querySelectorAll(".slide");
                    slides.forEach((slide, index) => {
                    slide.hidden = (window.dataStore.mode === 'presentation' && index !== window.dataStore.active_slide);
                    });

                    console.log('here') 
                    //show all components
                   const components = document.querySelectorAll(".component");
                    components.forEach((component, index) => {
                    component.hidden = false;
                     });

              //      console.log('Reverse Full before '  + outerContainer.offsetWidth + '  ' +  originalFontSizes[i]*originalWidth + 'px, after ' +fontSize  + 'px');
                });
            }
        }
        outerContainer.requestFullscreen().then(adjustFontSize)

       

}

document.getElementById('full-screen').addEventListener('click', function() {
    fullScreen();
});


});