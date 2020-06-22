
from django.urls import path,include
from . import views
from rest_framework import routers

from .views import SongViewSet

app_name= 'myapp'

router = routers.DefaultRouter()
#the following is the viewset view used with class based Model viewset
router.register('songlistviewset',views.SongViewSet,basename='Songlistviewset')


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
    path('api/',include(router.urls)),


    #testing the function based api view for a list of objects
    path('api/song-list-general/',views.song_list_general,name="song-list-general"),

    #testing the functin based api view for a single object
    path('api/song-detail-general/'+"<int:pk>",views.song_detail,name="song-detail-general"),


    #testing class based API views
    path('api/song-list-apiview/',views.SongAPIView.as_view(),name='song-list-apiview'),
    #testing class based API views for detail
    path('api/song-detail-apiview/'+'<int:pk>',views.SongDetailAPIView.as_view(),name='song-detail-apiview'),


    #testing class based API views (Mixins)
    path('api/song-list-mixin/',views.SongListMixin.as_view(),name='song-list-mixin'),
    #testing class based API views for detail (Mixins)
    path('api/song-detail-mixin/'+'<int:pk>',views.SongDetailMixin.as_view(),name='song-detail-mixin'),

    #testing class based API views (Generic)
    path('api/song-list-generic/',views.SongListGeneric.as_view(),name='song-list-generic'),
    #testing class based API views for detail (Mixins)
    path('api/song-detail-generic/'+'<int:pk>',views.SongDetailGeneric.as_view(),name='song-detail-generic'),

    #Register API
    path('api/register',views.RegisterAPI.as_view(),name='user-register'),

    #Login API
    path('api/login',views.LoginAPI.as_view(),name='user-login')

]
