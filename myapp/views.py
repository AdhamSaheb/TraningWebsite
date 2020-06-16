from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Song
# Create your views here.
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from .forms import UserForm, LoginForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def index(request):
    context_dect = {
        'songs': Song.objects.all(),
    }
    return render(request, 'myapp/index.html', context_dect)


def about(request):
    return render(request, 'myapp/about.html')


# Detail for every song

class song(DetailView):
    model = Song
    template_name = "myapp/song.html"


# This is a model form to add a song
@method_decorator(login_required, name='dispatch')
class CreateSong(CreateView):
    model = Song
    fields = ['name', 'likes', 'album', 'isFavorite', 'logo']


# This is a model form to Update a song

class UpdateSong(UpdateView):
    model = Song
    fields = ['name', 'likes', 'album', 'isFavorite', 'logo']


class DeleteSong(DeleteView):
    model = Song
    success_url = reverse_lazy('myapp:index')


# List view of all songs
@method_decorator(login_required, name='dispatch')
class songs(ListView):
    login_required = True
    template_name = 'myapp/songs.html'

    def get_queryset(self):
        return Song.objects.all()


# to register a User
class UserFormView(View):
    form_class = UserForm
    template_name = 'myapp/register.html'

    def get(self, request):
        # None means we're passing nothing with the form
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            # Now we authenticate the user
            user = authenticate(username=username, password=password)
            # this will return None if user in not authenticated
            # if it returned a value
            if user is not None:
                if user.is_active:  # if it's not banned/deleted ....
                    login(request, user)
                    # return redirect('myapp:index',{'user':user})
                    return render(request, 'myapp/index.html', {})
        return render(request, self.template_name, {'form': form})


class LoginFormView(View):
    form_class = LoginForm
    template_name = 'myapp/login.html'

    def get(self, request):
        # None means we're passing nothing with the form
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():
            # get clean data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Now we authenticate the user
            user = authenticate(username=username, password=password)
            # this will return None if user in not authenticated
            # if it returned a value
            if user is not None:
                if user.is_active:  # if it's not banned/deleted ....
                    login(request, user)
                    # return redirect('myapp:index',{'user':user})
                    return render(request, 'myapp/index.html', {})

        return render(request, self.template_name, {'form': form, 'error_msg': 'Incorrect Email or Password'})


def logout_request(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return redirect("myapp:index")


# Everything down from here is related to the API created

from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from .serializers import SongSerializer, GeneralSongSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status


# this is the general view for serializers, not generic or viewset type, and only shows the list
# @csrf_exempt # this decorator allows you to do the post request even if the csrf token is not proivded
@api_view(['GET', 'POST'])
def song_list_general(request):
    """
    List all code songs, or create a new song.
    """
    if request.method == 'GET':
        songs = Song.objects.all()
        serializer = GeneralSongSerializer(songs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = GeneralSongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # 201 is a created response
            return Response(serializer.data, status=201)
        # internal server error response
        return Response(serializer.errors, status=400)


# The next function will allow you to return a JSON response of only one object with a provided pk in the url
# it will have get,put and delete methods
@csrf_exempt
@api_view(('GET', 'PUT', 'DELETE'))
def song_detail(request, pk):
    try:
        song = Song.objects.get(pk=pk)
    except Song.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SongSerializer(song)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = SongSerializer(song, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        # internal server error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'DELETE':
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Next, are implementations for Class-Based API views , there are Mixin views, APIViews and Generic API Views

from rest_framework.views import APIView


class SongAPIView(APIView):

    def get(self, request):
        songs = Song.objects.all()
        serializer = GeneralSongSerializer(songs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GeneralSongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # 201 is a created response
            return Response(serializer.data, status=201)
        # internal server error response
        return Response(serializer.errors, status=400)


class SongDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        # try:
        #     song = Song.objects.get(pk=pk)
        # except Song.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        song= self.get_object(pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        song = self.get_object(pk)
        serializer = SongSerializer(song, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        song = self.get_object(pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# this class is general, it only allows you to get,post and put on the object(ViewSet class)
# one more note is that you can call the url /pk as well to view a specific object
# viewset will show the GUI of rest framework, the general one will only show you the data ( its an API view by default )
class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Songs to be viewed or edited.
    """
    queryset = Song.objects.all().order_by('id')  #
    serializer_class = SongSerializer  # this and the other serializer also works
