var btnUpload_img = $("#inputUpImage"),
		btnOuter_img = $(".button_outer_img");
	btnUpload_img.on("change", function(e){
		var ext = btnUpload_img.val().split('.').pop().toLowerCase();
		if($.inArray(ext, ['gif','png','jpg','jpeg']) == -1) {
			$(".error_msg_img").text("Not an Image...");
		} else {
			$(".error_msg_img").text("");
			btnOuter_img.addClass("file_uploading_img");
			setTimeout(function(){
				btnOuter_img.addClass("file_uploaded_img");
			},3000);
			var uploadedFile_img = URL.createObjectURL(e.target.files[0]);
			setTimeout(function(){
				$("#uploaded_view_img").append('<img src="'+uploadedFile_img+'" />').addClass("show");
			},3500);
		}
	});
	$(".file_remove_img").on("click", function(e){
		$("#uploaded_view_img").removeClass("show");
		$("#uploaded_view_img").find("img").remove();
		btnOuter_img.removeClass("file_uploading_img");
		btnOuter_img.removeClass("file_uploaded_img");
	});
//======================================================================================================

var btnUpload_vid = $("#inputUpVideo"),
	btnOuter_vid = $(".button_outer_vid");
	btnUpload_vid.on("change", function(e){
		var ext = btnUpload_vid.val().split('.').pop().toLowerCase();
		if($.inArray(ext, ['mp4','mpg','mpeg','avi','wmv','mov','rm','ram','swf','flv','ogg','webm','mpeg4']) == -1) {
			$(".error_msg_vid").text("Not an Video...");
		} else {
			$(".error_msg_vid").text("");
			btnOuter_vid.addClass("file_uploading_vid");
			setTimeout(function(){
				btnOuter_vid.addClass("file_uploaded_vid");
			},3000);
			var uploadedFile_vid = URL.createObjectURL(e.target.files[0]);
			setTimeout(function(){
				$("#uploaded_view_vid").append('<source src="'+uploadedFile_vid+'" />').addClass("show");
			},3500);
		}
	});
	$(".file_remove_vid").on("click", function(e){
		$("#uploaded_view_vid").removeClass("show");
		$("#uploaded_view_vid").find("video").remove();
		btnOuter_vid.removeClass("file_uploading_vid");
		btnOuter_vid.removeClass("file_uploaded_vid");
	});
	