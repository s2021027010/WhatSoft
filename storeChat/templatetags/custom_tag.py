from django import template 
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


from storeChat.models import db_Profile, SMS_Chat, Friend_Request
from storeChat.models import db_Write_Post, Like_Write , Comment_Write , Share_Write
from storeChat.models import db_Image_Post, Like_Image , Comment_Image , Share_Image
from storeChat.models import db_Video_Post, Like_Video , Comment_Video , Share_Video

register = template.Library()


# -------------------------------------------<< >>-------------------------------------------------------
@register.filter
def like_count_wrt(value):
    count = Like_Write.objects.filter(Like_Write_ForKey = value).all().count() 
    return count



@register.filter
def comment_count_wrt(value):
    count = Comment_Write.objects.filter(Comment_Write_ForKey = value).all().count()
    return count
 
 
@register.filter
def share_count_wrt(value):
    count = Share_Write.objects.filter(Share_Write_ForKey = value).all().count() 
    return count
# -------------------------------------------<< >>-------------------------------------------------------
@register.filter
def like_count_Img(value):
    count = Like_Image.objects.filter(Like_Image_ForKey = value).all().count() 
    return count


@register.filter
def comment_count_Img(value):
    count = Comment_Image.objects.filter(Comment_Image_ForKey = value).all().count() 
    return count

@register.filter
def share_count_Img(value):
    count = Share_Image.objects.filter(Share_Image_ForKey = value).all().count() 
    return count


# -------------------------------------------<< >>-------------------------------------------------------
@register.filter
def like_count_vid(value):
    count = Like_Video.objects.filter(Like_Video_ForKey = value).all().count() 
    return count


@register.filter
def comment_count_vid(value):
    count = Comment_Video.objects.filter(Comment_Video_ForKey = value).all().count() 
    return count

@register.filter
def share_count_vid(value):
    count = Share_Video.objects.filter(Share_Video_ForKey = value).all().count() 
    return count


# -------------------------------------------<< sms >>-------------------------------------------------------
'''
@register.filter
def Msg(value):
    sms = SMS_Chat.objects.values('sms_text').filter(email_sms_reciever = value).first()
    print(sms) 
    return sms
 
 '''