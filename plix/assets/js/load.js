import {render_patch} from './plix.js';



window.addEventListener('load', async function() {

  let isIFrame = false;
  let isFirstConnection = true;
  
  //This is when data is sent through an iFrame
  window.addEventListener('message', function(event) {
    const binaryData = event.data; // This is the ArrayBuffer received

    
    if (binaryData instanceof ArrayBuffer) {
        // Ensure msgpackr is available and then unpack the data
        try {
            const unpackedData = msgpackr.unpack(new Uint8Array(binaryData));


            const data = [{op: 'add', path: '/slides', value: unpackedData.slides}];
            console.log("Received data:",data);
        
            try {
                const patchResult = jsonpatch.applyPatch(window.dataStore.presentation, data);
                window.dataStore.presentation = patchResult.newDocument;
                //console.log('Patch applied successfully. New document: ',window.dataStore.presentation);
              } catch (error) {
                console.error('Error applying JSON patch:', error);
              }

              render_patch(data);

            isIFrame = true;
        } catch (error) {
            console.error("Error unpacking data:", error);
	}}
});


    
    function connectWebSocket() {
     
    
        try {
            const ws = new WebSocket(`ws://localhost:8889/data?isFirstConnection=${isFirstConnection}`);
            ws.binaryType = 'arraybuffer'; // Set the WebSocket to receive binary data

    
            ws.onopen = function(event) {
                console.log("Connected to WebSocket.");
                isFirstConnection = false; // Reset the flag after establishing the connection
               
            };
    
            ws.onmessage = function(event) {
                let data
                //data = JSON.parse(event.data).patch

                if (event.data instanceof ArrayBuffer) {
                    // Decode the MessagePack data
                    data = msgpackr.unpack(new Uint8Array(event.data));
                    //console.log('received: ' + data) 
                    // Now 'data' is your deserialized object
                } else {
                    console.error('Received data is not in binary format');
                }

                console.log("Message received.");
                //render_presentation(data);

                 // Apply patch
                try {
                  const patchResult = jsonpatch.applyPatch(window.dataStore.presentation, data);
                  window.dataStore.presentation = patchResult.newDocument;
                  //console.log('Patch applied successfully. New document: ',window.dataStore.presentation);
                } catch (error) {
                  console.error('Error applying JSON patch:', error);
                }

                render_patch(data);


            };
    
            ws.onerror = function(event) {
              //  console.error("WebSocket error observed. Attempting to reconnect...");
                // Do not initiate reconnect here, let onclose handle it
            };
    
            ws.onclose = function(event) {
                //console.log("WebSocket connection closed. Attempting to reconnect...");
                if (!isIFrame){
                setTimeout(connectWebSocket, 1000); // Exponential backoff
                }
            };
        } catch (error) {
            if (!isIFrame){
            setTimeout(connectWebSocket, 1000); // Exponential backoff
        }
        }
    }
    
  
     connectWebSocket()

     

})
