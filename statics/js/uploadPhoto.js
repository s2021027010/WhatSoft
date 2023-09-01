function trgger(e){
    document.getElementById(e).click();
    new Showprogress();
  }
  function Showprogress() {
      var indicator = document.querySelector('div.indicator'); 
      var preview = document.querySelector('div.preview');
      var divand = document.createElement('div');
      divand.setAttribute('id', 'progressand');
      divand.style.display = "none";	
      indicator.appendChild(divand);
      var div = document.createElement('div');
      div.setAttribute('class', 'progress');
      divand.appendChild(div);
      var dynamic = document.createElement('div');
      dynamic.setAttribute('id', 'dynamic');
      dynamic.setAttribute('class', 'progress-bar progress-bar-striped bg-info progress-bar-animated');
      dynamic.setAttribute('role', 'progressbar');
      dynamic.setAttribute('aria-valuenow', '0');
      dynamic.setAttribute('aria-valuemin', '0');
      dynamic.setAttribute('aria-valuemax', '100');
      dynamic.style.width = "0%";
      div.appendChild(dynamic);
      var percent = document.createElement('span');
      percent.setAttribute('class', 'percent');
      percent.textContent = '0%';
      dynamic.appendChild(percent);
      var load = document.createElement('div');
      load.setAttribute('class', 'ml-auto mr-auto lds-contuner');
      load.setAttribute('id', 'loader');
      load.style.display = "none";
      preview.appendChild(load);
      var loader = document.createElement('div');
      loader.setAttribute('class', 'lds-ellipsis');
      load.appendChild(loader);	
     for (let x = 0; x < 4; x++) {
        var divm = document.createElement('div');
        loader.appendChild(divm);
     }
  }
  function previewFiles() {
     var preview = document.querySelector('div.preview');
     var files   = document.querySelector('input[type=file]').files;
     function readAndPreview(file) {
        if ( /\.(jpe?g|png|gif|mp4|webm|ogg|ogv|mp3|wav)$/i.test(file.name)) {	
          if (file.size < 10 * 1024 * 1024) { // MAX 10 mb
               var reader = new FileReader();
               var spc = '\u00A0';
                  function returnFileSize(n) {
                     if(n < 1024) {
                        return n + ' octets';
                     } else if(n >= 1024 && n < 1048576) {
                        return (n/1024).toFixed(1)+spc+'Ko';
                     } else if(n >= 1048576) {
                        return (n/1048576).toFixed(1)+spc+'Mo';
                     }
                  }
                  function abortRead() {
                     reader.abort();
                  }
                  reader.onloadstart = function(e) {
                 document.querySelector("#progressand").style.display = "block";
                 document.querySelector("#loader").style.display = "block";
              }
                  reader.onprogress = function(e) {
                     if (e.lengthComputable) {
                        var percentLoaded = Math.round((e.loaded / e.total) * 99);
                        if (percentLoaded < 99) {
                          document.querySelector('#dynamic').style.width = percentLoaded + '%';
                          document.querySelector('.percent').textContent = percentLoaded + '%';
                        }
                     }
                  }
                  reader.onloadend = function(e) {
                      document.querySelector('#dynamic').style.width = '100%';
                      document.querySelector('.percent').textContent = '100%';
                      setTimeout(function(){
                 $("#progressand").remove();	
                 $("#loader").remove();	
                      }, 900);
              }
                 reader.onabort = function(e) {
                    return iziError(failed, 'File read cancelled');
                 }
               reader.addEventListener('error', function ()  {
                     return iziError(failed, 'Error occurred reading file: ${file.name}');
               })	   
               reader.addEventListener("load", function () {
                   var div = document.createElement('div');
                   div.setAttribute('class', 'Imgpreview mb-3');// animated zoomIn
                   preview.appendChild(div);
                   var i = document.createElement('i');
                   i.setAttribute('class', 'material-icons remove');
                   i.textContent = "close";
                   div.appendChild(i);
                   if ( /\.(jpe?g|png|gif|)$/i.test(file.name)) {
                       var image = new Image();
                 //image.addEventListener("load", function () {/*image.width+'×'+image.height*/})
                       image.setAttribute('data-tippy-content',file.name+spc+'\u002f'+spc+'file size'+spc+returnFileSize(file.size));
                 image.setAttribute('onclick', 'this.classList.toggle("Imgpreview-zoom");');
                       image.src = this.result;
                       div.appendChild(image);
                 } else if ( /\.(mp4|webm|ogg|ogv)$/i.test(file.name)) {
                       var video = document.createElement('video');
                       video.setAttribute('width', '100%');
                       video.setAttribute('data-tippy-content',file.name+spc+'\u002f'+spc+'file size'+spc+returnFileSize(file.size));
                 video.setAttribute('onclick', 'this.classList.toggle("Imgpreview-zoom");');
                       video.muted = false;
                       video.volume = 0;
                       video.autoplay = true;
                       video.loop = true;
                       video.preload = "auto";
                       video.src = this.result;
                       div.appendChild(video);
                 } else if ( /\.(mp3|wav|ogg)$/i.test(file.name)) {
                     var audio = document.createElement('audio');
                     audio.setAttribute('data-tippy-content', file.name+spc+'\u002f'+spc+'file size'+spc+returnFileSize(file.size));
                     audio.setAttribute('controlslist', 'nodownload');
                     audio.controls = true;
                     audio.preload = "auto";
                     audio.src = this.result;
                     div.appendChild(audio);
                 }
                 tippy([image, video, audio]);
                   $(i).click(function(){
                     $(div).removeClass('zoomIn').addClass('flipOutX');// hinge
                     setTimeout(function(){$(i).parent(div).remove();},500);
                   });
               }, false);
               reader.readAsDataURL(file);  
           } else {
               return iziToast.error({title: 'failed',message: 'max 10 MB',iconText: 'error_outline'});
           } 
        } else {
          return  iziToast.error({title: 'failed',message: 'Please provide avalid file. Accepted formats include .mp4, mp3, .png, .jpg, and .gif.',iconText: 'error_outline'});
        }
     } if (files) {
        [].forEach.call(files, readAndPreview);
     }
  }
  autosize(document.querySelectorAll('textarea'));
  