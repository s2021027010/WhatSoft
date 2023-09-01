$(document).on('submit', "#post-form_{{myPost_Wrt.id}}", function(e){
        e.preventDefault();
        var input_id_Like_wrt = "{{myPost_Wrt.id}}"
        var input_sender_email_wrt = "{{myPost_Wrt.db_username_post}}"
        var input_shareby_email_wrt = "{{user.email}}"
            //data = data.file('post-form')
            $.ajax({
                type: 'post',
                url : "/like_wrt/",

                data: {
                        input_id_Like_wrt: input_id_Like_wrt,
                        input_sender_email_wrt: input_sender_email_wrt,
                        input_shareby_email_wrt: input_shareby_email_wrt,
                                    
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
            });
                        
    });
                        
