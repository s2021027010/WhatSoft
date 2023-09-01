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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from storeChat.models import db_Profile, SMS_Chat, Friend_Request
from storeChat.models import db_Write_Post, Like_Write , Comment_Write , Share_Write
from storeChat.models import db_Image_Post, Like_Image , Comment_Image , Share_Image
from storeChat.models import db_Video_Post, Like_Video , Comment_Video , Share_Video

import sys , os
from .views import *
from . import views


from django.views import View
from django.urls import reverse_lazy


def logIn(request):
    #template = loader.get_template('account/logIn.html')
    '''if request.user.is_authenticated:
        return redirect('newsfeed')
    else:'''
    if request.method == 'POST':
            var_Email = request.POST.get('input_Email')
            var_password = request.POST.get('input_password')

            user_obj = User.objects.filter(username = var_Email).first()
            if (len(var_password) >= 6):
                if user_obj is None:
                    messages.error(request, 'User not found.')
                    return redirect('logIn')
                
                
                profile_obj = db_Profile.objects.filter(db_email = user_obj ).first()

                if not profile_obj.is_verified:
                    messages.error(request, 'User is not verified check your mail.')
                    return redirect('logIn')

                user = authenticate(username = var_Email , password = var_password)
                if user is  None:
                    messages.error(request, 'Wrong password.')
                    return redirect('logIn')
                
                login(request , user)
                global gb_userIn
                gb_userIn = var_Email
                last_login(var_Email)
                return redirect('newsfeed')
            else:
                messages.error(request, 'Password Must be six charatcer Long')
            
    context = {}
    return render(request , 'account/logIn.html', context)
            #return HttpResponse(template.render(context, request))
        
def last_login(email):
    loginUpdate = db_Profile.objects.get(char_email = email)
    dattim = str(datetime.datetime.today())
    loginUpdate.db_last_login = dattim
    loginUpdate.save()

def initialize(): 
    global gb_username
    gb_username = gb_userIn



# -------------------------------------- ----------------------- reset Password Start ---------------------- //


def forgotPassword(request):

    if request.method == 'POST': 
        input_email = request.POST['input_email']
        input_password = request.POST['resetPassword']
        input_confirmPassword = request.POST['confirmPassword']

        user = User.objects.filter(username = input_email , email = input_email).first()

    
        if input_password != input_confirmPassword:
            messages.error(request,"Password Didn't Match")
        if user is None:
            messages.error(request, "Email Didn't Match")
        if (len(input_password) <= 5):
            messages.error(request, "Password must be Six Character Long")
        else:
            try:
                user_obj = User.objects.get(username = input_email, email = input_email)
                profile_obj = db_Profile.objects.filter(char_email = input_email).first()
                
                myuser = db_Profile.objects.get(char_email = input_email)
                
                if user_obj is None:
                    messages.error(request, 'User not found.')
                else:
                    profile_obj.is_verified = False
                    auth_token = profile_obj.auth_token
                    user_obj.set_password(input_password)
                    myuser.is_verified = False

                    profile_obj.save()
                    user_obj.save()
                    myuser.save()
                    messages.success(request, 'Email Successfully Reset Password, \n We have sent an email to you , \"Please check your mail to Verify\"')
                    send_mail_after_registration(input_email , auth_token)
                    return redirect('logIn')
                        
            except Exception as e:
                print(e)
    return render(request , 'account/forgotPassword.html')
    

# -------------------------------------- ----------------------- reset Password Start ---------------------- //


def changePassword(request):  
    template = loader.get_template('account/changePassword.html') 
    #if request.user.is_authenticated:
    profile_post = db_Profile.objects.filter(char_email = gb_userIn).all()
    if request.method == "POST":  
        input_email = request.POST['input_email']
        input_Oldpassword = request.POST['input_password']
        input_NewPassword = request.POST['input_NewPassword']
        input_ConfirmPassword = request.POST['input_ConfirmPassword']

        profile_obj = db_Profile.objects.get(char_email= input_email)
        user_obj = User.objects.filter(username = input_email).first()
        user = authenticate(username = input_email , password = input_Oldpassword)
        if user_obj is not None:
            myuser = db_Profile.objects.get(char_email = input_email)
        
        if user_obj is None:
            messages.error(request, 'User not found.')
            return redirect('changePassword')
        elif user is None:
            messages.error(request, 'Invalid password.')
            return redirect('changePassword')
        elif (len(input_NewPassword) <= 5):
            messages.error(request, "New Password must be Six Character Long")
        elif input_NewPassword != input_ConfirmPassword:
            messages.error(request, "Password didn't Match.")
            return redirect('changePassword')
        else:
            try:
                user_obj.set_password(input_NewPassword)
                user_obj.save()

                messages.success(request, 'Password Successfully Save Changed.')
                logOut(request, input_email)
                return redirect('logIn') 

            except Exception as e:
                print(e)
    context = {
        'profile_post' : profile_post,
    }
    return HttpResponse(template.render(context, request))





# -------------------------------------- ----------------------- Sign Up Start ---------------------- //


def signUp(request):
    date = str(datetime.date.today())
    dattim = str(datetime.datetime.today())
    if request.user.is_authenticated:
        return redirect('newsfeed')
    else:
        if request.method == 'POST':
            db_Email = request.POST.get('input_Email')
            if len(request.FILES) != 0:
                db_photo =  request.FILES['input_imageP']
            db_FName = request.POST.get('input_FName')
            db_LName = request.POST.get('input_LName')
            db_password = request.POST.get('input_password')
            db_ConfirmPassword = request.POST.get('input_ConfirmPassword')
            db_Gender = request.POST.get('input_Gender')
            db_Ph_number = request.POST.get('input_Ph_number')
            db_Country = request.POST.get('input_Country')
            db_date_DoB = request.POST.get('input_DoB')


            if db_date_DoB > date :
                messages.error(request,"Date must be before present date.")
                return redirect('signUp')
            elif len(db_Ph_number) >= 13:
                messages.error(request,"Phone number Must be under 13 Digits.")
                return redirect('signUp')
            elif not (len(db_password) >= 6):
                messages.error(request,"Password Must be six charatcer Long")
                return redirect('signUp')
            else:
                if db_password != db_ConfirmPassword:
                    messages.error(request,"Password Didn't Match")
                    return redirect('signUp')
        try:
            if User.objects.filter(email = db_Email).first():
                messages.error(request, 'Email is already Taken.')
                return redirect('signUp')
            
            if User.objects.filter(username = db_Email).first():
                    messages.error(request, 'Username is already Taken.')
                    return redirect('signUp')
                
            user_obj = User(username = db_Email , email = db_Email)
            user_obj.first_name = db_FName
            user_obj.last_name = db_LName
            user_obj.set_password(db_password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = db_Profile.objects.create(db_email = user_obj ,
            auth_token = auth_token,
            char_email = db_Email,
            db_gender = db_Gender,
            db_photo = db_photo,
            db_firstName = db_FName,
            db_lastName = db_LName,
            db_phoneNumber = db_Ph_number,
            db_address = db_Country,
            db_date_DoB = db_date_DoB,
            db_last_login = dattim,
            db_last_logout = dattim,
            )

            profile_obj.save()
            send_mail_after_registration(db_Email , auth_token)
            messages.success(request, 'Email Successfully Register. \n We have sent an email to you , \"Please check your mail to Verify\"')
            return redirect('logIn')
        except Exception as e:
            print(e)
        return render(request=request, template_name="account/signUp.html", context={ })


def verify(request , auth_token):
    try:
        profile_obj = db_Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('logIn')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('logIn')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'account/error.html')

def send_mail_after_registration(email , token):
    subject = 'WhatSoft : Activation Code'
    domain = settings.LOCAL_HOST_STRIPE
    message = f'Welcome to WhatSoft !! \n Hi {email}, \n Please confirm your email by clicking on the following link.\n \n Confirmation Link: {domain}/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from , recipient_list, fail_silently = True )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signUp')
    else:
        return render(request,'activation_failed.html')



# -------------------------------------- ----------------------- Sign Up Start ---------------------- //
 

@login_required
def logOut(request,email):
    last_logout(email)
    request.session.clear()
    logout(request)
    return redirect('logIn')

def last_logout(email):
    logOutUpdate = db_Profile.objects.get(char_email = email)
    dattim = str(datetime.datetime.today())
    logOutUpdate.db_last_logout = dattim
    logOutUpdate.save()
