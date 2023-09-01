var loadFile = function(event) {
    var image = document.getElementById('input_imageP');
    
    var upl = image;
        var max = 1*1024*1024;

        if(event.target.files[0].size >= max)
        {
                alert("File too big!  max(1Mb)");
                upl.value = "";
        }else{
                image.src = URL.createObjectURL(event.target.files[0]);
        }
    var upl_pub = document.getElementById("input_imageApp");
        var max = 1*1024*1024;

        if(event.target.files[0].size  >= max)
            {
                alert("File too big!  max(1Mb)");
                upl_pub.value = "";
            }
            else{
                image.src = URL.createObjectURL(event.target.files[0]);
        }
        
    
};