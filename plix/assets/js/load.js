import {render_slides} from './plix.js';




document.addEventListener('DOMContentLoaded', function() {
  function setupSSE() {
    const eventSource = new EventSource("http://localhost:8889/events");

    eventSource.onopen = () => {
 //     console.log("SSE connection established.");
    };

    eventSource.onmessage = (event) => {
      if (event.data === "ready") {
      //  console.log("Server is ready. Connecting WebSocket...");
        connectWebSocket();
      }
    };

   // eventSource.onerror = (error) => {
   //   console.error("SSE connection error:", error);
   //   console.log("Attempting to reconnect...");
      // The browser retries automatically, no manual logic needed here
    //};
  }

  function connectWebSocket() {
    const ws = new WebSocket("ws://localhost:8889/data");
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
  //    console.log("WebSocket connection opened.");
    };

    ws.onmessage = (event) => {
      const binaryData = event.data;
      const unpackedData = msgpackr.unpack(new Uint8Array(binaryData));
      render_slides(unpackedData);
     // console.log("Received WebSocket data:", unpackedData);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

   // ws.onclose = () => {
   //   console.warn("WebSocket connection closed.");
   // };
  }

  // Start listening for readiness via SSE
  setupSSE();
  
});


// window.addEventListener('load', async function() {

//   let isIFrame = false;
//   let isFirstConnection = true;
  
//   //This is when data is sent through an iFrame
//   window.addEventListener('message', function(event) {
//     const binaryData = event.data; // This is the ArrayBuffer received

    
//     if (binaryData instanceof ArrayBuffer) {
//         // Ensure msgpackr is available and then unpack the data
//         try {
//             const unpackedData = msgpackr.unpack(new Uint8Array(binaryData));


//             const data = [{op: 'add', path: '/slides', value: unpackedData.slides}];
//             console.log("Received data:",data);
        
//             try {
//                 const patchResult = jsonpatch.applyPatch(window.dataStore.presentation, data);
//                 window.dataStore.presentation = patchResult.newDocument;
//                 //console.log('Patch applied successfully. New document: ',window.dataStore.presentation);
//               } catch (error) {
//                 console.error('Error applying JSON patch:', error);
//               }
//               console.log(data)
//               render_patch(data);

//             isIFrame = true;
//         } catch (error) {
//             console.error("Error unpacking data:", error);
// 	}}
// });



//   // Apply JSON Patch
//   //try {
//   //    const patchResult = jsonpatch.applyPatch(window.dataStore.presentation, data);
//   //    window.dataStore.presentation = patchResult.newDocument;
//   //    console.log('Patch applied successfully. New document:', window.dataStore.presentation);
//   //} catch (error) {
//   //    console.error('Error applying JSON patch:', error);
//  // }

//   // Render updated state
//   //ender_patch(data);
// };
  


// //     function connectWebSocket() {
     
    
// //         try {
// //             const ws = new WebSocket(`ws://localhost:8889/data?isFirstConnection=${isFirstConnection}`);
// //             ws.binaryType = 'arraybuffer'; // Set the WebSocket to receive binary data

    
// //             ws.onopen = function(event) {
// //                 console.log("Connected to WebSocket.");
// //                 isFirstConnection = false; // Reset the flag after establishing the connection
               
// //             };
    
// //             ws.onmessage = function(event) {
// //                 let data
// //                 //data = JSON.parse(event.data).patch

// //                 if (event.data instanceof ArrayBuffer) {

// //                     // Decode the MessagePack data
// //                     data = msgpackr.unpack(new Uint8Array(event.data));
                    
// //                 } else {
// //                     console.error('Received data is not in binary format');
// //                 }

// //                 console.log("Message received.");

// //                  // Apply patch
// //                 try {
                 
// //                   const patchResult = jsonpatch.applyPatch(window.dataStore.presentation, data);
// //                   window.dataStore.presentation = patchResult.newDocument;
                 
// //                   console.log('Patch applied successfully. New document: ',window.dataStore.presentation);
// //                 } catch (error) {
// //                   console.error('Error applying JSON patch:', error);
// //                 }
             
// //                 console.log(data)
// //                 render_patch(data);


// //             };
    
// //             ws.onerror = function(event) {
// //               //  console.error("WebSocket error observed. Attempting to reconnect...");
// //                 // Do not initiate reconnect here, let onclose handle it
// //             };
    
// //             ws.onclose = function(event) {
// //                 //console.log("WebSocket connection closed. Attempting to reconnect...");
// //                 if (!isIFrame){
// //                 setTimeout(connectWebSocket, 1000); // Exponential backoff
// //                 }
// //             };
// //         } catch (error) {
// //             if (!isIFrame){
// //             setTimeout(connectWebSocket, 1000); // Exponential backoff
// //         }
// //         }
// //     }
    
  
// //      connectWebSocket()

     

//  })
