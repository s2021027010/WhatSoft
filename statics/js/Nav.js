
//----------------------------------------------------------------------------------------------

function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
  }
   
  function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
  }


//----------------------------------------------------------------------------------------------
inputUpImage.onchange = evt => {
  const [file] = inputUpImage.files
  
  if (file) {
      img.src = URL.createObjectURL(file)
      }
  }