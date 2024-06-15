
window.addEventListener('load', async function() {


//document.getElementById('share').addEventListener('click', function() {
//    fetch("/share")
 //       .then(response => response.text())
  //      .then(url => {
   //         showModal(url);
   //     })
   //     .catch(error => {
    //        console.error("Error fetching share URL:", error);
    //    });
//});

// Initialize clipboard
//const clipboard = new ClipboardJS('#copyBtn');

//clipboard.on('success', function(e) {
 //   const modalText = document.getElementById('modalText');
 //   modalText.textContent = "Copied to clipboard!";
    
  //  setTimeout(() => {
  //      closeModal(); // Close the modal after 1.5 seconds
  //  }, 1500);
    
   // e.clearSelection();
//});


//function showModal(text) {
//    const modal = document.getElementById('customModal');
//    const modalText = document.getElementById('modalText');
//    const copyBtn = document.getElementById('copyBtn');

 //   modalText.textContent = text;
 //   copyBtn.setAttribute('data-clipboard-text', text); // set the clipboard text for the button
 //   modal.style.display = 'block';

    // This will close the modal if you click outside of it
  //  window.onclick = function(event) {
   //     if (event.target === modal) {
   //         closeModal();
   //     }
   // }
//}

//function closeModal() {
 //   const modal = document.getElementById('customModal');
 //   modal.style.display = 'none';
//}



//function downloadJSONData() {
 //   const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data.data));
  //  const downloadAnchorNode = document.createElement('a');
   // downloadAnchorNode.setAttribute("href", dataStr);
 //   downloadAnchorNode.setAttribute("download", "presentation.plx");
 //   document.body.appendChild(downloadAnchorNode); 
 //   downloadAnchorNode.click(); 
 //   downloadAnchorNode.remove();
//}

//document.getElementById('download').addEventListener('click', function() {
//    downloadJSONData();
//});

})