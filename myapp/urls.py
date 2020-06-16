
from django.urls import path,include
from . import views
from rest_framework import routers

from .views import SongViewSet

app_name= 'myapp'

router = routers.DefaultRouter()
router.register('songlist',views.SongViewSet,basename='Songlist')


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

    #a path for user registration
    path('register/', views.UserFormView.as_view(),name='register'),

    # a path for user login
    path('login/', views.LoginFormView.as_view(), name='login'),

    path('about/', views.about,name='about'),






    #this will redirect every url starting with api to the router
    #this will be related to all urls for the api testing
    path('api/',include(router.urls))
]
