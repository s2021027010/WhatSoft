from django.contrib import admin
# from WhatSoft.admin_site import custom_admin_site

# Register your models here.
from .models import db_Profile, SMS_Chat, Friend_Request
from .models import db_Write_Post, Like_Write , Comment_Write , Share_Write
from .models import db_Image_Post, Like_Image , Comment_Image , Share_Image
from .models import db_Video_Post, Like_Video , Comment_Video , Share_Video



class SMS_Inline(admin.TabularInline):
    model = SMS_Chat
class Friend_Inline(admin.TabularInline):
    model = Friend_Request

class db_SMS_Friend_Inline(admin.ModelAdmin):
    inlines = [SMS_Inline, Friend_Inline]

admin.site.register(db_Profile, db_SMS_Friend_Inline)

#------------------------------------- Write >>>  Like / Sahre /Comment ------------------------
class Like_Write_Inline(admin.TabularInline):
    model = Like_Write

class Comment_Write_Inline(admin.TabularInline):
    model = Comment_Write

class Share_Write_Inline(admin.TabularInline):
    model = Share_Write

class db_Write_Inline(admin.ModelAdmin):
    inlines = [Like_Write_Inline, Comment_Write_Inline, Share_Write_Inline]


admin.site.register(db_Write_Post, db_Write_Inline)


#------------------------------------- Image >>>  Like / Sahre /Comment ------------------------

class Like_Image_Inline(admin.TabularInline):
    model = Like_Image

class Comment_Image_Inline(admin.TabularInline):
    model = Comment_Image

class Share_Image_Inline(admin.TabularInline):
    model = Share_Image

class db_Image_Inline(admin.ModelAdmin):
    inlines = [Like_Image_Inline, Comment_Image_Inline, Share_Image_Inline]

admin.site.register(db_Image_Post, db_Image_Inline)


#------------------------------------- Video >>>  Like / Share /Comment ------------------------
class Like_Video_Inline(admin.TabularInline):
    model = Like_Video

class Comment_Video_Inline(admin.TabularInline):
    model = Comment_Video

class Share_Video_Inline(admin.TabularInline):
    model = Share_Video

class db_Video_Inline(admin.ModelAdmin):
    inlines = [Like_Video_Inline, Comment_Video_Inline, Share_Video_Inline]


admin.site.register(db_Video_Post, db_Video_Inline)