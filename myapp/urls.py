"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

app_name= 'myapp'


urlpatterns = [
    path('', views.index, name='index'),
    #get all songs (List View)
    path("songs/",views.songs.as_view(),name='songs'),

    #get song details
    path("songs/"+"<int:pk>",views.song.as_view(),name='song'),

    #Create a song Model
    path("songs/Create",views.CreateSong.as_view(),name='CreateSong'),

    # Update a song Model
    path("songs/update/"+"<int:pk>",views.UpdateSong.as_view(),name='UpdateSong'),\

    # Delete a song Model
    path("songs/delete/"+"<int:pk>",views.DeleteSong.as_view(),name='DeleteSong'),
    #user logout
    path("logout", views.logout_request, name="logout"),

    #a path for user registeration
    path('register/', views.UserFormView.as_view(),name='register'),




    path('about/', views.about,name='about'),
]
