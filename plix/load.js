import {render_presentation} from './render.js';



window.addEventListener('load', async function() {

    let isFirstConnection = true;
  
    
    function connectWebSocket() {
     
    
        try {
            const ws = new WebSocket(`ws://localhost:8888/data?isFirstConnection=${isFirstConnection}`);
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
                //    console.log('received: ' + data) 
                    // Now 'data' is your deserialized object
                } else {
                    console.error('Received data is not in binary format');
                }

                console.log("Message received.");
                render_presentation(data);
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
})