from fileinput import FileInput
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
import uuid, re
from . tokens import generate_token

from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from WhatSoft import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from storeChat.models import db_Profile, SMS_Chat, Friend_Request
from storeChat.models import db_Write_Post, Like_Write , Comment_Write , Share_Write
from storeChat.models import db_Image_Post, Like_Image , Comment_Image , Share_Image
from storeChat.models import db_Video_Post, Like_Video , Comment_Video , Share_Video

import sys , os
from pathlib import Path

from . import views
from .views import *
from . import account
# from . import custom_tag

from django.views import View
from django.urls import reverse_lazy



 
#@login_required(login_url='logIn')
def newsfeed(request):
    template = loader.get_template('Tab_Page/newsfeed.html')
    if request.method == 'POST':
        var_id = request.POST.get('input_Id')
        var_Email = request.POST.get('input_Email')
        var_post = request.POST.get('input_Post')
        var_status =  request.POST.get('input_Status')
        img =  request.POST.get('inputUpImage')
        vid =  request.POST.get('inputUpVideo')
        

        if len(request.FILES) != 0:
            if img is None:
                var_image =  request.FILES['inputUpImage']
                Img_Post(request, var_id, var_Email, var_post, var_image, var_status)
                return redirect('/newsfeed/')
            else:
                var_image = ""
            if vid is None and img == "":
                var_video = request.FILES['inputUpVideo']
                Vid_Post(request, var_id, var_Email, var_post, var_video, var_status)
                return redirect('/newsfeed/')
            else:
                var_video = ""
        else:
            var_image = ""
            var_video = ""
            Wrt_Post(request, var_id, var_Email, var_post, var_status)
            return redirect('/newsfeed/')
    
    
    account.initialize()
    #if request.user.is_authenticated:
    obj_profile = db_Profile.objects.filter(char_email = account.gb_username).all()

    profile_post = db_Profile.objects.all().values()
    Wrt_Post_obj = db_Write_Post.objects.all().values()
    Img_Post_obj = db_Image_Post.objects.all().values()
    Vid_Post_obj = db_Video_Post.objects.all().values()
    Wrt_Post_like = db_Write_Post.objects.all()
    Wrt_Post_model = db_Write_Post.objects.all()
    Comment_wrt = Comment_Write.objects.all()
    Comment_img = Comment_Image.objects.all() 
    Comment_vid = Comment_Video.objects.all() 
    Share_wrt = Share_Write.objects.all() 
    Share_wrt_show = Share_Write.objects.all()
     
     
    context = {
        'obj_profile' : obj_profile,
        'Wrt_Post_obj' : Wrt_Post_obj,
        'Img_Post_obj' : Img_Post_obj,
        'Vid_Post_obj' : Vid_Post_obj,
        'profile_post' : profile_post,
        'Wrt_Post_model' : Wrt_Post_model,
        'Wrt_Post_like' : Wrt_Post_like, 
        'Comment_wrt' : Comment_wrt,
        'Comment_img' : Comment_img,
        'Comment_vid' : Comment_vid,
        'Share_wrt' : Share_wrt, 
        'Share_wrt_show': Share_wrt_show,

    }
    return HttpResponse(template.render(context, request))


#@login_required(login_url='logIn')
def search(request):
    
    search = request.GET['search']
    profile_post = db_Profile.objects.all().values()
    # mySearch = db_Write_Post.objects.filter(db_AppName__contains = search.capitalize()) | db_Write_Post.objects.filter(db_Category__contains = search.capitalize() ).values() 
    mySearch_profile = db_Profile.objects.filter(char_email__contains = search) | db_Profile.objects.filter(db_firstName__contains = search) |  db_Profile.objects.filter(db_lastName__contains = search).values()
    mySearch_Write = db_Write_Post.objects.filter(db_username_post__contains = search) | db_Write_Post.objects.filter(db_text_post__contains = search) |  db_Write_Post.objects.filter(db_id_post__contains = search).values() | db_Write_Post.objects.filter(db_type_post__contains = search).values() 
    mySearch_Img = db_Image_Post.objects.filter(db_username_image__contains = search) | db_Image_Post.objects.filter(db_text_image__contains = search) |  db_Image_Post.objects.filter(db_id_image__contains = search).values() | db_Image_Post.objects.filter(db_type_image__contains = search).values() 
    mySearch_Vid = db_Video_Post.objects.filter(db_username_video__contains = search) | db_Video_Post.objects.filter(db_text_video__contains = search) |  db_Video_Post.objects.filter(db_id_video__contains = search).values() | db_Video_Post.objects.filter(db_type_video__contains = search).values() 
    template = loader.get_template('Tab_Page/search.html')
    context = {
        'profile_post': profile_post,
        'mySearch_profile': mySearch_profile,
        'mySearch_Write': mySearch_Write,
        'mySearch_Img': mySearch_Img,
        'mySearch_Vid': mySearch_Vid,
    }
     
    return HttpResponse(template.render(context, request))

 



def Wrt_Post(request, pk, email ,post, status):
    if post != "":
        Write_Post_obj = db_Write_Post.objects.create(db_username_post = email ,
            db_id_post = pk,
            db_text_post = post,
            db_status_post = status,
            db_type_post = "Write",
            value_comment_post = "CommentPost",
            value_share_post = "SharePost",
            )
        Write_Post_obj.save()
        messages.success(request, 'Your Written Post are successfully Uploaded.')
        return redirect('Tab_Page/newsfeed.html')
    else:
        return redirect('Tab_Page/newsfeed.html')

 
def Img_Post(request, pk, email ,post, image, status):  
    if image != "":
        exe = os.path.splitext(str(image))
        file_exe = exe[1]
        if (file_exe == ".jpg") or (file_exe == ".jpng") or (file_exe == ".jpeg") or (file_exe == ".png") or (file_exe == ".gif") or (file_exe == ".cr2") or (file_exe == ".nef") or (file_exe == ".orf") or (file_exe == ".sr2") or (file_exe == ".bmp") or (file_exe == ".tif") or (file_exe == ".tiff") or (file_exe == ".raw") or (file_exe == ".eps") or (file_exe == ".AI") or (file_exe == ".psd"):
            Post_image_obj = db_Image_Post.objects.create(db_username_image = email ,
                db_id_image = pk,
                db_text_image = post,
                db_status_image = status,
                db_type_image = "Image",
                db_images = image,
                value_comment_image = "CommentImage",
                value_share_Image = "ShareImage",
                )
            Post_image_obj.save()
            messages.success(request, 'Your Image Post are successfully Uploaded.')

def Vid_Post(request, pk, email ,post, video, status):
    if video != "":
        exe = os.path.splitext(str(video))
        file_exe = exe[1]
        if (file_exe == ".mp4") or (file_exe == ".ogg") or (file_exe == ".webm") or (file_exe == ".mpeg4") or (file_exe == ".flv") or (file_exe == ".mpg") or (file_exe == ".mpeg") or (file_exe == ".avi") or (file_exe == ".wmv") or (file_exe == ".rm") or (file_exe == ".mov") or (file_exe == ".swf"):
            Post_video_obj = db_Video_Post.objects.create(db_username_video = email ,
                db_id_video = pk,
                db_text_video = post,
                db_status_video = status,
                db_type_video = "Video",
                db_link_video = video,
                value_comment_video = "CommentVideo",
                value_share_video = "ShareVideo",
                )
            Post_video_obj.save()
            messages.success(request, 'Your Video Post are successfully Uploaded.')
        
#@login_required(login_url='logIn')
def chat(request):
    template = loader.get_template('Tab_Page/chat.html')

    account.initialize()
    #if request.user.is_authenticated:
    obj_profile = db_Profile.objects.filter(char_email = account.gb_username).all()

    sms_obj_both = SMS_Chat.objects.filter().all()
    profile_post = db_Profile.objects.filter().all()
    Chat_sms_obj = SMS_Chat.objects.filter( ).all() 
    
    context = {
        'obj_profile' : obj_profile,
        'profile_post' : profile_post,
        'Chat_sms_obj' : Chat_sms_obj,
        'sms_obj_both' : sms_obj_both,
    }
    return HttpResponse(template.render(context, request))

       
#@login_required(login_url='logIn')
def message(request, email):
    template = loader.get_template('Tab_Page/message.html')
    account.initialize()
    #if request.user.is_authenticated:
    obj_profile = db_Profile.objects.filter(char_email = account.gb_username).all()
    
    
    if request.method == 'POST':
        forKey_sms = request.POST.get('input_forKey_sms') 
        sender_email = account.gb_username
        sms_Text = request.POST.get('input_sms_text')
        reciever_email = request.POST.get('input_email_reciever_sms')
        #value  = Reciever/Sender
        sms_To(request, forKey_sms, sender_email, sms_Text, reciever_email)


    profile_post_sms = db_Profile.objects.filter(char_email = email).all()
    profile_post = db_Profile.objects.filter().all()
    sms_obj_both = SMS_Chat.objects.filter().all() 
    
    context = {
        'obj_profile' : obj_profile,
        'profile_post_sms' : profile_post_sms,
        'profile_post' : profile_post, 
        'sms_obj_both' : sms_obj_both,
    }
    return HttpResponse(template.render(context, request))


def sms_To(request, forKey_sms, sender_email, sms_Text, reciever_email):
    smsProfile_obj_reciever = db_Profile.objects.get(char_email= sender_email)
    smsProfile_obj_sender = db_Profile.objects.get(char_email= reciever_email)
    user_reciever = get_object_or_404(User, username = reciever_email )
    user_sender = get_object_or_404(User, username = sender_email)

    db_sms_chat = SMS_Chat(sms_ForKey_id = forKey_sms, email_sms_reciever = reciever_email, email_sms_sender = sender_email, sms_text = sms_Text )
        
    if SMS_Chat.objects.filter(email_sms_sender = sender_email).exists() == True:
        db_sms_chat.value = 'Reciever' + "" + str(forKey_sms)
        smsProfile_obj_reciever.db_sms_reciever.add(user_reciever)
        smsProfile_obj_sender.db_sms_sender.add(user_sender)
        db_sms_chat.save()
    else:
        db_sms_chat.value = 'Reciever' + "" + str(forKey_sms)
        smsProfile_obj_reciever.db_sms_reciever.add(user_reciever)
        smsProfile_obj_sender.db_sms_sender.add(user_sender)
        db_sms_chat.save()
    

#@login_required(login_url='logIn')
def photo(request):
    template = loader.get_template('Tab_Page/photo.html')
    
    if request.method == 'POST':
        var_id = request.POST.get('input_Id')
        var_Email = request.POST.get('input_Email')
        var_post = request.POST.get('input_Post')
        var_status =  request.POST.get('input_Status')
        img =  request.POST.get('inputUpImage') 
        

        if len(request.FILES) != 0:
            if img is None:
                var_image =  request.FILES['inputUpImage']
                Img_Post(request, var_id, var_Email, var_post, var_image, var_status)
                return redirect('profile')
            else:
                var_image = ""
        else:
            var_image = "" 
    
    
    account.initialize()
    #if request.user.is_authenticated:
    obj_profile = db_Profile.objects.filter(char_email = account.gb_username).all()

    profile_post = db_Profile.objects.all().values()
    Wrt_Post_obj = db_Write_Post.objects.all().values()
    Img_Post_obj = db_Image_Post.objects.all().values()
    Vid_Post_obj = db_Video_Post.objects.all().values()
    Wrt_Post_like = db_Write_Post.objects.all()
    Wrt_Post_model = db_Write_Post.objects.all()
    Comment_wrt = Comment_Write.objects.all()
    Comment_img = Comment_Image.objects.all() 
    Comment_vid = Comment_Video.objects.all() 
    Share_wrt = Share_Write.objects.all() 
     
     
    context = {
        'obj_profile' : obj_profile,
        'Wrt_Post_obj' : Wrt_Post_obj,
        'Img_Post_obj' : Img_Post_obj,
        'Vid_Post_obj' : Vid_Post_obj,
        'profile_post' : profile_post,
        'Wrt_Post_model' : Wrt_Post_model,
        'Wrt_Post_like' : Wrt_Post_like, 
        'Comment_wrt' : Comment_wrt,
        'Comment_img' : Comment_img,
        'Comment_vid' : Comment_vid,
        'Share_wrt' : Share_wrt, 

    }
    return HttpResponse(template.render(context, request))

#@login_required(login_url='logIn')
def watch(request):
    template = loader.get_template('Tab_Page/watch.html')
    if request.method == 'POST':
        var_id = request.POST.get('input_Id')
        var_Email = request.POST.get('input_Email')
        var_post = request.POST.get('input_Post')
        var_status =  request.POST.get('input_Status')
        img =  request.POST.get('inputUpImage')
        vid =  request.POST.get('inputUpVideo')
        

        if len(request.FILES) != 0:
            if img is None:
                var_image =  request.FILES['inputUpImage'] 
            else:
                var_image = ""
            if vid is None and img == "":
                var_video = request.FILES['inputUpVideo']
                Vid_Post(request, var_id, var_Email, var_post, var_video, var_status)
                return redirect('profile')
            else:
                var_video = ""
        else:
            var_image = ""
    
    
    account.initialize()
    #if request.user.is_authenticated:
    obj_profile = db_Profile.objects.filter(char_email = account.gb_username).all()

    profile_post = db_Profile.objects.all().values()
    Wrt_Post_obj = db_Write_Post.objects.all().values()
    Img_Post_obj = db_Image_Post.objects.all().values()
    Vid_Post_obj = db_Video_Post.objects.all().values()
    Wrt_Post_like = db_Write_Post.objects.all()
    Wrt_Post_model = db_Write_Post.objects.all()
    Comment_wrt = Comment_Write.objects.all()
    Comment_img = Comment_Image.objects.all() 
    Comment_vid = Comment_Video.objects.all() 
    Share_wrt = Share_Write.objects.all() 
     
     
    context = {
        'obj_profile' : obj_profile,
        'Wrt_Post_obj' : Wrt_Post_obj,
        'Img_Post_obj' : Img_Post_obj,
        'Vid_Post_obj' : Vid_Post_obj,
        'profile_post' : profile_post,
        'Wrt_Post_model' : Wrt_Post_model,
        'Wrt_Post_like' : Wrt_Post_like, 
        'Comment_wrt' : Comment_wrt,
        'Comment_img' : Comment_img,
        'Comment_vid' : Comment_vid,
        'Share_wrt' : Share_wrt, 

    }
    return HttpResponse(template.render(context, request))

#@login_required(login_url='logIn')
def profile(request, email):
    template = loader.get_template('Tab_Page/profile.html')
    if request.method == 'POST':
        var_id = request.POST.get('input_Id')
        var_Email = request.POST.get('input_Email')
        var_post = request.POST.get('input_Post')
        var_status =  request.POST.get('input_Status')
        img =  request.POST.get('inputUpImage')
        vid =  request.POST.get('inputUpVideo')
        

        if len(request.FILES) != 0:
            if img is None:
                var_image =  request.FILES['inputUpImage']
                Img_Post(request, var_id, var_Email, var_post, var_image, var_status)
                return redirect('profile')
            else:
                var_image = ""
            if vid is None and img == "":
                var_video = request.FILES['inputUpVideo']
                Vid_Post(request, var_id, var_Email, var_post, var_video, var_status)
                return redirect('profile')
            else:
                var_video = ""
        else:
            var_image = ""
            var_video = ""
            Wrt_Post(request, var_id, var_Email, var_post, var_status)
            return redirect('profile')
    
    
    account.initialize()
    #if request.user.is_authenticated:
    obj_profile = db_Profile.objects.filter(char_email = email).all()

    profile_post = db_Profile.objects.all().values()
    Wrt_Post_obj = db_Write_Post.objects.filter(db_username_post = email).all().values()
    Img_Post_obj = db_Image_Post.objects.filter(db_username_image = email).all().values()
    Vid_Post_obj = db_Video_Post.objects.filter(db_username_video = email).all().values()
    Wrt_Post_like = db_Write_Post.objects.all()
    Wrt_Post_model = db_Write_Post.objects.all()
    Comment_wrt = Comment_Write.objects.all()
    Comment_img = Comment_Image.objects.all() 
    Comment_vid = Comment_Video.objects.all() 
    Share_wrt = Share_Write.objects.all() 
     
     
    context = {
        'obj_profile' : obj_profile,
        'Wrt_Post_obj' : Wrt_Post_obj,
        'Img_Post_obj' : Img_Post_obj,
        'Vid_Post_obj' : Vid_Post_obj,
        'profile_post' : profile_post,
        'Wrt_Post_model' : Wrt_Post_model,
        'Wrt_Post_like' : Wrt_Post_like, 
        'Comment_wrt' : Comment_wrt,
        'Comment_img' : Comment_img,
        'Comment_vid' : Comment_vid,
        'Share_wrt' : Share_wrt, 

    }
    return HttpResponse(template.render(context, request))


#@login_required(login_url='logIn')
def friend(request):
    template = loader.get_template('Tab_Page/friend.html')
    account.initialize()
    if request.method == 'POST':
        Friend_forKey = request.POST.get('input_forKey_Friend')
        email_request_sender = account.gb_username
        email_request_reciever = request.POST.get('input_email_request_Reciever')
        friend_Request_reciever(request, Friend_forKey, email_request_sender, email_request_reciever)
        # friend_Request_sender(request, Friend_forKey, email_request_sender, email_request_reciever)



    #if request.user.is_authenticated:
    obj_profile = db_Profile.objects.filter(char_email = account.gb_username).all()

    profile_post = db_Profile.objects.filter().all() 
    Friend_post = Friend_Request.objects.filter().all() 
    
    context = {
        'obj_profile' : obj_profile, 
        'profile_post' : profile_post,
        'Friend_post' : Friend_post,
    }
    return HttpResponse(template.render(context, request))


def friend_Request_reciever(request, Friend_forKey, email_request_sender, email_request_reciever):
    post_obj_reciever = db_Profile.objects.get(char_email = email_request_reciever )
    user_reciever = get_object_or_404(User, username = email_request_sender) 
    post_obj_sender = db_Profile.objects.get(char_email = email_request_sender )
    user_sender = get_object_or_404(User, username = email_request_reciever)

    Friend = Friend_Request(Friend_ForKey_id = Friend_forKey, email_friend_request_sender = email_request_sender , email_friend_request_reciever = email_request_reciever)
        
        
    if Friend_Request.objects.filter( email_friend_request_sender = email_request_sender , email_friend_request_reciever = email_request_reciever).exists() == True:
        db_Friend_Del = Friend_Request.objects.get( email_friend_request_sender = email_request_sender , email_friend_request_reciever = email_request_reciever)
        db_Friend_Del.delete()
        post_obj_sender.db_friend_sender.remove(user_sender)
        post_obj_reciever.db_friend_reciever.remove(user_reciever)
    else:
        Friend.value = 'Friend'
        post_obj_sender.db_friend_sender.add(user_sender)
        post_obj_reciever.db_friend_reciever.add(user_reciever)  
        Friend.save()
    success = 'Friend Request Successfully Send to ' + email_request_reciever
    return redirect('/friend/')
 

#@login_required(login_url='logIn')
def header(request):
    template = loader.get_template('header.html')
    
    account.initialize()
    #if request.user.is_authenticated:
    obj_profile = db_Profile.objects.filter(char_email = account.gb_username).all()
    context = {
        'obj_profile' : obj_profile,
    }
    return HttpResponse(template.render(context, request))



# ===========================================<<   Likee  >>=============================================================


def like_wrt(request):
    if request.method == 'POST':
        forKey_Like_post = request.POST.get('input_forKey_Like_wrt')
        id_Like_post = request.POST.get('input_id_Like_wrt')
        sender_email = request.POST.get('input_sender_email_wrt')
        shareby_email = request.POST.get('input_shareby_email_wrt')
        post_obj = db_Write_Post.objects.get(id =  id_Like_post )
        user = get_object_or_404(User, username = shareby_email) 

        db_Like_wrt = Like_Write(Like_Write_ForKey_id = forKey_Like_post, db_id_Like_Write = id_Like_post , email_liked_Write_sender = sender_email , email_liked_Write_by = shareby_email)
        
        
        if Like_Write.objects.filter(db_id_Like_Write = id_Like_post ,email_liked_Write_by = shareby_email).exists() == True:
            db_Like_Del = Like_Write.objects.get(db_id_Like_Write = id_Like_post, email_liked_Write_by = shareby_email)
            db_Like_Del.delete()
            post_obj.db_like_post.remove(user)
        else:
            db_Like_wrt.value = 'LikePost'
            post_obj.db_like_post.add(user)
            db_Like_wrt.save()
        local = settings.LOCAL_HOST_STRIPE
        success = 'Successfully liked'
    return redirect('/newsfeed/')



def like_Img(request):
    if request.method == 'POST':
        forKey_Like_post = request.POST.get('input_forKey_Like_Img')
        id_Like_post = request.POST.get('input_id_Like_Img')
        sender_email = request.POST.get('input_sender_email_Img')
        shareby_email = request.POST.get('input_shareby_email_Img')
        post_obj = db_Image_Post.objects.get(id = id_Like_post)
        user = get_object_or_404(User, username = shareby_email)

        db_Like_img = Like_Image(Like_Image_ForKey_id = forKey_Like_post, db_id_Like_Image = id_Like_post , email_liked_Image_sender = sender_email , email_liked_Image_by = shareby_email)
        
        
        if Like_Image.objects.filter(db_id_Like_Image = id_Like_post ,email_liked_Image_by = shareby_email).exists() == True:
            db_Like_Del = Like_Image.objects.get(db_id_Like_Image = id_Like_post, email_liked_Image_by = shareby_email)
            db_Like_Del.delete()
            post_obj.db_like_image.remove(user)
        else:
            db_Like_img.value = 'LikeImage'
            post_obj.db_like_image.add(user)
            db_Like_img.save()
        local = settings.LOCAL_HOST_STRIPE

    return redirect('/newsfeed/')



def like_vid(request):
    if request.method == 'POST':
        forKey_Like_post = request.POST.get('input_forKey_Like_vid')
        id_Like_post = request.POST.get('input_id_Like_vid')
        sender_email = request.POST.get('input_sender_email_vid')
        shareby_email = request.POST.get('input_shareby_email_vid')
        post_obj = db_Video_Post.objects.get(id = id_Like_post)
        user = get_object_or_404(User, username = shareby_email)

        db_Like_vid = Like_Video(Like_Video_ForKey_id = forKey_Like_post, db_id_Like_Video = id_Like_post , email_liked_Video_sender = sender_email , email_liked_Video_by = shareby_email)
        
        
        if Like_Video.objects.filter(db_id_Like_Video = id_Like_post ,email_liked_Video_by = shareby_email).exists() == True:
            db_Like_Del = Like_Video.objects.get(db_id_Like_Video = id_Like_post, email_liked_Video_by = shareby_email)
            db_Like_Del.delete()
            post_obj.db_like_video.remove(user)
        else:
            db_Like_vid.value = 'LikeVideo'
            post_obj.db_like_video.add(user)
            db_Like_vid.save()
        local = settings.LOCAL_HOST_STRIPE

    return redirect('/newsfeed/')



# ===========================================<<   Share  >>=============================================================


def Share_wrt(request):
    if request.method == 'POST':
        forKey_Share_post = request.POST.get('input_forKey_Share_wrt')
        id_Share_post = request.POST.get('input_id_Share_wrt')
        sender_email = request.POST.get('input_sender_email_wrt')
        shareby_email = request.POST.get('input_shareby_email_wrt')
        post_obj = db_Write_Post.objects.get(id = id_Share_post)
        user = get_object_or_404(User, username = shareby_email)

        db_Share_wrt = Share_Write(Share_Write_ForKey_id = forKey_Share_post, db_id_share_Write = id_Share_post , email_share_Write_sender = sender_email , email_share_Write_by = shareby_email)
        
        
        if Share_Write.objects.filter(db_id_share_Write = id_Share_post ,email_share_Write_by = shareby_email).exists() == True:
            db_Share_wrt.value_share_Write = 'SharePost' + "" + id_Share_post
            post_obj.db_share_post.add(user)
            post_obj.value_share_post = "SharePost" + "" + id_Share_post
            post_obj.save()
            db_Share_wrt.save()
        else:
            db_Share_wrt.value_share_Write = 'SharePost' + "" + id_Share_post
            post_obj.db_share_post.add(user)
            post_obj.value_share_post = "SharePost" + "" + id_Share_post
            post_obj.save()
            db_Share_wrt.save()
        # local = settings.LOCAL_HOST_STRIPE

    return redirect('/newsfeed/')



def Share_Img(request):
    if request.method == 'POST':
        forKey_Share_post = request.POST.get('input_forKey_Share_Img')
        id_Share_post = request.POST.get('input_id_Share_Img')
        sender_email = request.POST.get('input_sender_email_Img')
        shareby_email = request.POST.get('input_shareby_email_Img')
        post_obj = db_Image_Post.objects.get(id = id_Share_post)
        user = get_object_or_404(User, username = shareby_email)

        db_Share_Img = Share_Image(Share_Image_ForKey_id = forKey_Share_post, db_id_share_Image = id_Share_post , email_share_Image_sender = sender_email , email_share_Image_by = shareby_email)
        
        
        if Share_Image.objects.filter(db_id_share_Image = id_Share_post , email_share_Image_by = shareby_email).exists() == True:
            db_Share_Img.value_share_Image = 'ShareImage' + "" + id_Share_post
            post_obj.db_share_image.add(user)
            post_obj.value_share_Image = "ShareImage" + "" + id_Share_post
            post_obj.save()
            db_Share_Img.save()
        else:
            db_Share_Img.value_share_Image = 'ShareImage' + "" + id_Share_post
            post_obj.db_share_image.add(user)
            post_obj.value_share_Image = "ShareImage" + "" + id_Share_post
            post_obj.save()
            db_Share_Img.save()
        local = settings.LOCAL_HOST_STRIPE

    return redirect('/newsfeed/')



def Share_vid(request):
    if request.method == 'POST':
        forKey_Share_post = request.POST.get('input_forKey_Share_vid')
        id_Share_post = request.POST.get('input_id_Share_vid')
        sender_email = request.POST.get('input_sender_email_vid')
        shareby_email = request.POST.get('input_shareby_email_vid')
        post_obj = db_Video_Post.objects.get(id = id_Share_post)
        user = get_object_or_404(User, username = shareby_email)

        db_Share_vid = Share_Video(Share_Video_ForKey_id = forKey_Share_post, db_id_share_Video = id_Share_post , email_share_Video_sender = sender_email , email_share_Video_by = shareby_email)
        
        
        if Share_Video.objects.filter(db_id_share_Video = id_Share_post , email_share_Video_by = shareby_email).exists() == True:
            db_Share_vid.value_share_Video = 'ShareVideo' + "" + id_Share_post
            post_obj.db_share_video.add(user)
            post_obj.value_share_video = "ShareVideo" + "" + id_Share_post
            post_obj.save()
            db_Share_vid.save()
        else:
            db_Share_vid.value_share_Video = 'ShareVideo' + "" + id_Share_post
            post_obj.db_share_video.add(user)
            post_obj.value_share_video = "ShareVideo" + "" + id_Share_post
            post_obj.save()
            db_Share_vid.save()
        local = settings.LOCAL_HOST_STRIPE

    return redirect('/newsfeed/')



# ===========================================<<   Comment  >>=============================================================




def Comment_wrt(request):
    if request.method == 'POST':
        forKey_Comment_post = request.POST.get('input_forKey_Comment_wrt')
        id_Comment_post = request.POST.get('input_id_Comment_wrt')
        sender_email = request.POST.get('input_sender_email_wrt')
        shareby_email = request.POST.get('input_shareby_email_wrt')
        comment_wrt = request.POST.get('input_comment_wrt')
        post_obj = db_Write_Post.objects.get(id = id_Comment_post)
        user = get_object_or_404(User, username = shareby_email)

        db_Comment_wrt = Comment_Write(Comment_Write_ForKey_id = forKey_Comment_post, db_id_comment_Write = id_Comment_post , comment_Text_Write = comment_wrt ,email_comment_Write_sender = sender_email , email_comment_Write_by = shareby_email)
        
        
        if Comment_Write.objects.filter(db_id_comment_Write = id_Comment_post , email_comment_Write_by = shareby_email).exists() == True:
            db_Comment_wrt.value_comment_Write = 'CommentPost' + "" + id_Comment_post
            post_obj.db_comment_post.add(user)
            post_obj.value_comment_post = 'CommentPost' + "" + id_Comment_post
            post_obj.save()
            db_Comment_wrt.save()
        else:
            db_Comment_wrt.value_comment_Write = 'CommentPost' + "" + id_Comment_post
            post_obj.db_comment_post.add(user)
            post_obj.value_comment_post = 'CommentPost' + "" + id_Comment_post
            post_obj.save()
            db_Comment_wrt.save()
        local = settings.LOCAL_HOST_STRIPE

    return redirect('/newsfeed/')


def Comment_Img(request):
    if request.method == 'POST':
        forKey_Comment_post = request.POST.get('input_forKey_Comment_Img')
        id_Comment_post = request.POST.get('input_id_Comment_Img')
        sender_email = request.POST.get('input_sender_email_Img')
        shareby_email = request.POST.get('input_shareby_email_Img')
        comment_wrt = request.POST.get('input_comment_Img')
        post_obj = db_Image_Post.objects.get(id = id_Comment_post)
        user = get_object_or_404(User, username = shareby_email)

        db_Comment_Img = Comment_Image(Comment_Image_ForKey_id = forKey_Comment_post, db_id_comment_Image = id_Comment_post , comment_Text_Image = comment_wrt , email_comment_Image_sender = sender_email , email_comment_Image_by = shareby_email)
        
        
        if Comment_Image.objects.filter(db_id_comment_Image = id_Comment_post , email_comment_Image_by = shareby_email).exists() == True:
            db_Comment_Img.value_comment_Image = 'CommentImage' + "" + id_Comment_post
            post_obj.db_comment_image.add(user)
            post_obj.value_comment_image = 'CommentImage' + "" + id_Comment_post
            post_obj.save()
            db_Comment_Img.save()
        else:
            db_Comment_Img.value_comment_Image = 'CommentImage' + "" + id_Comment_post
            post_obj.db_comment_image.add(user)
            post_obj.value_comment_image = 'CommentImage' + "" + id_Comment_post
            post_obj.save()
            db_Comment_Img.save()
        local = settings.LOCAL_HOST_STRIPE

    return redirect('/newsfeed/')


def Comment_vid(request):
    if request.method == 'POST':
        forKey_Comment_post = request.POST.get('input_forKey_Comment_vid')
        id_Comment_post = request.POST.get('input_id_Comment_vid')
        sender_email = request.POST.get('input_sender_email_vid')
        shareby_email = request.POST.get('input_shareby_email_vid')
        comment_wrt = request.POST.get('input_comment_vid')
        post_obj = db_Video_Post.objects.get(id = id_Comment_post)
        user = get_object_or_404(User, username = shareby_email)

        db_Comment_vid = Comment_Video(Comment_Video_ForKey_id = forKey_Comment_post, db_id_comment_Video = id_Comment_post , comment_Text_Video = comment_wrt , email_comment_Video_sender = sender_email , email_comment_Video_by = shareby_email)

        
        if Comment_Video.objects.filter(db_id_comment_Video = id_Comment_post , email_comment_Video_by = shareby_email).exists() == True:
            db_Comment_vid.value_comment_Video = 'CommentVideo' + "" + id_Comment_post
            post_obj.db_comment_video.add(user)
            post_obj.value_comment_video = "CommentVideo" + "" + id_Comment_post
            post_obj.save()
            db_Comment_vid.save()
        else:
            db_Comment_vid.value_comment_Video = 'CommentVideo' + "" + id_Comment_post
            post_obj.db_comment_video.add(user)
            post_obj.value_comment_video = "CommentVideo" + "" + id_Comment_post
            post_obj.save()
            db_Comment_vid.save()
        local = settings.LOCAL_HOST_STRIPE

    return redirect('/newsfeed/')


