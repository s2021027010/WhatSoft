from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views import View
import sys , os

from . import views
from . import account

from django.urls import include, path
from django.conf.urls import include

urlpatterns = [
    path('' , account.logIn, name='logIn'),
    path('signUp/' , account.signUp, name='signUp'),
    path('activate/<uidb64>/<token>', account.activate, name='activate'),
    path('verify/<auth_token>' , account.verify , name="verify"),
    path('account/error' , account.error_page , name="error"),
    path('logOut/<str:email>', account.logOut, name='logOut'),
    path('forgotPassword/', account.forgotPassword, name='forgotPassword'),
    path('changePassword/', account.changePassword, name='changePassword'),

    #path('/home/' , views.home, name='home'),
    path('header/' , views.header, name='header'),
    path('newsfeed/' , views.newsfeed, name='newsfeed'),
    path('chat/' , views.chat, name='chat'),
    path('message/<str:email>' , views.message, name='message'),
    path('photo/' , views.photo, name='photo'),
    path('watch/' , views.watch, name='watch'),
    path('friend/' , views.friend, name='friend'),
    path('search/', views.search, name='search'),

    path('profile/<str:email>' , views.profile, name='profile'),

    
    path('like_wrt/', views.like_wrt, name='like_wrt'),
    path('like_Img/', views.like_Img, name='like_Img'),
    path('like_vid/', views.like_vid, name='like_vid'),

    path('Share_wrt/', views.Share_wrt, name='Share_wrt'),
    path('Share_Img/', views.Share_Img, name='Share_Img'),
    path('Share_vid/', views.Share_vid, name='Share_vid'),

    path('Comment_wrt/', views.Comment_wrt, name='Comment_wrt'),
    path('Comment_Img/', views.Comment_Img, name='Comment_Img'),
    path('Comment_vid/', views.Comment_vid, name='Comment_vid'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)