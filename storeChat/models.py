from asyncio.windows_events import NULL
from email.policy import default
from enum import auto
from datetime import datetime, time, date
from random import choices
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class db_Profile(models.Model):
    db_email = models.OneToOneField(User , on_delete=models.CASCADE)
    char_email = models.CharField(max_length=255)
    db_firstName = models.CharField(max_length=255)
    db_lastName = models.CharField(max_length=255)
    db_gender = models.CharField(max_length=125)
    db_phoneNumber = models.CharField(max_length=255)
    db_address = models.CharField(max_length=255)
    db_date_DoB = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    db_last_login = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True)
    db_last_logout = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True)
    db_photo = models.ImageField(upload_to = "Profile/", width_field=None, height_field=None, max_length=255, blank=True)
    
    db_sms_reciever = models.ManyToManyField(User, related_name='db_sms_reciever')
    db_sms_sender = models.ManyToManyField(User, related_name='db_sms_sender')
    db_friend_reciever = models.ManyToManyField(User, related_name='db_friend_reciever')
    db_friend_sender = models.ManyToManyField(User, related_name='db_friend_sender')
    auth_token = models.CharField(max_length=100 )
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    

    def __str__(self):
        return self.char_email
    #@property
   
    def get_user_by_email(email):
        try:
            return db_Profile.objects.get(char_email = email)
        except:
            return False
    def isExists(self):
        if db_Profile.objects.filter(User = self.char_email):
            return True
        return False 


#------------------------------------- >> Friend Request ----------------------------------------------



class Friend_Request(models.Model):
    Friend_ForKey = models.ForeignKey(db_Profile, on_delete=models.CASCADE) 
    email_friend_request_sender = models.CharField(max_length=255)  
    email_friend_request_reciever = models.CharField(max_length=255) 
    value = models.CharField(max_length=255) #Friend

    def __str__(self):
        return str(self.email_friend_request_sender)

    def isExists(self):
        if Friend_Request.objects.filter(val=self.value):
            return True
        return False


#------------------------------------- >> SmS Send ----------------------------------------------


class SMS_Chat(models.Model):
    sms_ForKey = models.ForeignKey(db_Profile, on_delete=models.CASCADE) 
    email_sms_sender = models.CharField(max_length=255)
    email_sms_reciever = models.CharField(max_length=255)
    sms_text = models.TextField(max_length = 50000)
    value = models.CharField(max_length=255) #SmS (Send/Recieve) 
    db_date_sms = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __str__(self):
        return str(self.email_sms_reciever)

    def isExists(self):
        if SMS_Chat.objects.filter(val=self.value):
            return True
        return False


#------------------------------------- Write >>>  Like / Share /Comment ------------------------
class db_Write_Post(models.Model):
    db_username_post = models.CharField(max_length=255)
    db_id_post = models.CharField(max_length=255)
    db_text_post = models.TextField(max_length=2000)
    db_status_post = models.CharField(max_length=255) #status(public, friend , private)
    db_type_post = models.CharField(max_length=255) #Write
    db_date_post = models.DateTimeField(auto_now_add = False, auto_now = True)
    
    db_like_post = models.ManyToManyField(User, related_name='db_like_post')

    db_comment_post = models.ManyToManyField(User, related_name='db_comment_post')
    value_comment_post = models.CharField(max_length=255) #CommentPost(Value)

    db_share_post = models.ManyToManyField(User, related_name='db_share_post')
    value_share_post = models.CharField(max_length=255) #SharePost(Value)

    def __str__(self):
        return (self.db_username_post) + " ::::: " + (self.db_text_post)
    
    @property
    def total_like_post(self):
        return self.db_like_post.all().count()
    
    @property
    def total_comment_post(self):
        return self.db_comment_post.all().count()
    
    @property
    def total_share_post(self):
        return self.db_share_post.all().count()
    
    def get_post_by_email(email_wrt):
        try:
            return db_Write_Post.objects.get(db_username_post = email_wrt)
        except:
            return False



class Like_Write(models.Model):
    Like_Write_ForKey = models.ForeignKey(db_Write_Post, on_delete=models.CASCADE)
    db_id_Like_Write = models.CharField(max_length=255)
    email_liked_Write_by = models.CharField(max_length=255)
    email_liked_Write_sender = models.CharField(max_length=255)
    value = models.CharField(max_length=255) #like 

    def __str__(self):
        return str(self.email_liked_Write_by)

    def isExists(self):
        if Like_Write.objects.filter(val=self.value):
            return True
        return False

class Share_Write(models.Model):
    Share_Write_ForKey = models.ForeignKey(db_Write_Post, on_delete=models.CASCADE)
    db_id_share_Write = models.CharField(max_length=255)
    email_share_Write_by = models.CharField(max_length=255)
    email_share_Write_sender = models.CharField(max_length=255)
    value_share_Write = models.CharField(max_length=255) #share


    def __str__(self):
        return str(self.db_id_share_Write + " ::: " + self.email_share_Write_by)

    def isExists(self):
        if Share_Write.objects.filter(val=self.db_id_share_Write):
            return True

        return False


class Comment_Write(models.Model):
    Comment_Write_ForKey = models.ForeignKey(db_Write_Post, on_delete=models.CASCADE)
    db_id_comment_Write = models.CharField(max_length=255)
    email_comment_Write_by = models.CharField(max_length=255)
    email_comment_Write_sender = models.CharField(max_length=255)
    comment_Text_Write = models.CharField(max_length=255)
    value_comment_Write = models.CharField(max_length=255) #CommentPost
    date_comment_Write = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__(self):
        return str(self.db_id_comment_Write + " ::: " + self.email_comment_Write_by)

    def isExists(self):
        if Comment_Write.objects.filter(val=self.value_comment_Write):
            return True
        return False



#------------------------------------- Image >>>  Like / Share /Comment ------------------------

class db_Image_Post(models.Model):
    db_username_image = models.CharField(max_length=255)
    db_id_image = models.CharField(max_length=255)
    db_text_image = models.TextField(max_length=2000)
    db_status_image = models.CharField(max_length=255) #status(public, friend , private)
    db_type_image = models.CharField(max_length=255) #Image
    db_date_image = models.DateTimeField(auto_now_add = False, auto_now = True)
    db_images = models.ImageField(upload_to = "PostImage/", width_field=None, height_field=None, max_length=255, blank=True)
     
    db_like_image = models.ManyToManyField(User, related_name='db_like_image')
    db_comment_image = models.ManyToManyField(User, related_name='db_comment_image')
    value_comment_image = models.CharField(max_length=255) #CommentImage(Value)

    db_share_image = models.ManyToManyField(User, related_name='db_share_image')
    value_share_Image = models.CharField(max_length=255) #ShareImage(Value)

   
    def __str__(self):
        return (self.db_username_image) + " ::::: " + (self.db_type_image)
   
    @property
    def total_like_image(self):
        return self.db_like_image.all().count()
    
    @property
    def total_comment_image(self):
        return self.db_comment_image.all().count()
    
    @property
    def total_share_image(self):
        return self.db_share_image.all().count()
    
    def get_image_by_email(email_img):
        try:
            return db_Image_Post.objects.get(db_username_image = email_img)
        except:
            return False


class Like_Image(models.Model):
    Like_Image_ForKey = models.ForeignKey(db_Image_Post, on_delete=models.CASCADE)
    db_id_Like_Image = models.CharField(max_length=255)
    email_liked_Image_by = models.CharField(max_length=255)
    email_liked_Image_sender = models.CharField(max_length=255)
    value = models.CharField(max_length=255) #like 

    def __str__(self):
        return str(self.email_liked_Image_by)

    def isExists(self):
        if Like_Image.objects.filter(val=self.value):
            return True

        return False

class Share_Image(models.Model):
    Share_Image_ForKey = models.ForeignKey(db_Image_Post, on_delete=models.CASCADE)
    db_id_share_Image = models.CharField(max_length=255)
    email_share_Image_by = models.CharField(max_length=255)
    email_share_Image_sender = models.CharField(max_length=255)
    value_share_Image = models.CharField(max_length=255) #share


    def __str__(self):
        return str(self.db_id_share_Image + " ::: " + self.email_share_Image_by)

    def isExists(self):
        if Share_Image.objects.filter(val=self.db_id_share_Image):
            return True

        return False


class Comment_Image(models.Model):
    Comment_Image_ForKey = models.ForeignKey(db_Image_Post, on_delete=models.CASCADE)
    db_id_comment_Image = models.CharField(max_length=255)
    email_comment_Image_by = models.CharField(max_length=255)
    email_comment_Image_sender = models.CharField(max_length=255)
    value_comment_Image = models.CharField(max_length=255)
    comment_Text_Image = models.CharField(max_length=255)
    date_comment_Image = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__(self):
        return str(self.db_id_comment_Image + " ::: " + self.email_comment_Image_by)

    def isExists(self):
        if Comment_Image.objects.filter(val=self.value_comment_Image):
            return True
        return False



#------------------------------------- Video >>>  Like / Share /Comment ------------------------


class db_Video_Post(models.Model):
    db_username_video = models.CharField(max_length=255)
    db_id_video = models.CharField(max_length=255)
    db_text_video = models.TextField(max_length=2000)
    db_status_video = models.CharField(max_length=255) #status(public, friend , private)
    db_type_video = models.CharField(max_length=255) #video
    db_link_video = models.ImageField(upload_to = "PostVideo/", width_field=None, height_field=None, max_length=255, blank=True)
    db_date_video = models.DateTimeField(auto_now_add = False, auto_now = True)
    
    db_like_video = models.ManyToManyField(User, related_name='db_like_video')
    db_comment_video = models.ManyToManyField(User, related_name='db_comment_video')
    value_comment_video = models.CharField(max_length=255) #CommentVideo(Value)

    db_share_video = models.ManyToManyField(User, related_name='db_share_video')
    value_share_video = models.CharField(max_length=255) #ShareVideo(Value)
    
    def __str__(self):
        return (self.db_username_video) + " ::::: " + (self.db_type_video)
   
    @property
    def total_like_video(self):
        return self.db_like_video.all().count()
    
    @property
    def total_comment_video(self):
        return self.db_comment_video.all().count()
    
    @property
    def total_share_video(self):
        return self.db_share_video.all().count()
    
    def get_image_by_email(email_vid):
        try:
            return db_Video_Post.objects.get(db_username_video = email_vid)
        except:
            return False



class Like_Video(models.Model):
    Like_Video_ForKey = models.ForeignKey(db_Video_Post, on_delete=models.CASCADE)
    db_id_Like_Video = models.CharField(max_length=255)
    email_liked_Video_by = models.CharField(max_length=255)
    email_liked_Video_sender = models.CharField(max_length=255)
    value = models.CharField(max_length=255) #like 

    def __str__(self):
        return str(self.email_liked_Video_by)

    def isExists(self):
        if Like_Video.objects.filter(val=self.value):
            return True

        return False

class Share_Video(models.Model):
    Share_Video_ForKey = models.ForeignKey(db_Video_Post, on_delete=models.CASCADE)
    db_id_share_Video = models.CharField(max_length=255)
    email_share_Video_by = models.CharField(max_length=255)
    email_share_Video_sender = models.CharField(max_length=255)
    value_share_Video = models.CharField(max_length=255) #share


    def __str__(self):
        return str(self.db_id_share_Video + " ::: " + self.email_share_Video_by)

    def isExists(self):
        if Share_Video.objects.filter(val=self.db_id_share_Video):
            return True

        return False


class Comment_Video(models.Model):
    Comment_Video_ForKey = models.ForeignKey(db_Video_Post, on_delete=models.CASCADE)
    db_id_comment_Video = models.CharField(max_length=255)
    email_comment_Video_by = models.CharField(max_length=255)
    email_comment_Video_sender = models.CharField(max_length=255)
    value_comment_Video = models.CharField(max_length=255)
    comment_Text_Video = models.CharField(max_length=255)
    date_comment_Video = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__(self):
        return str(self.db_id_comment_Video + " ::: " + self.email_comment_Video_by)

    def isExists(self):
        if Comment_Video.objects.filter(val=self.value_comment_Video):
            return True
        return False

