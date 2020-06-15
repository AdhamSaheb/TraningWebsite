from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Song
# Create your views here.
from django.views.generic import ListView,DetailView,View
from django.views.generic.edit import DeleteView,UpdateView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from .forms import UserForm
from django.shortcuts import redirect


def index(request):
    context_dect= {
        'songs': Song.objects.all(),
    }
    return render(request,'myapp/index.html',context_dect)


def about(request):
    return render(request,'myapp/about.html')


#Detail for every song

class song(DetailView):
    model = Song
    template_name = "myapp/song.html"

#This is a model form to add a song

class CreateSong(CreateView):
    model = Song
    fields = ['name', 'likes', 'album', 'isFavorite','logo']

#This is a model form to Update a song

class UpdateSong(UpdateView):
    model = Song
    fields = ['name', 'likes', 'album', 'isFavorite','logo']


class DeleteSong(DeleteView):
    model = Song
    success_url = reverse_lazy('myapp:index')



#List view of all songs
class songs(ListView):
    template_name = 'myapp/songs.html'

    def get_queryset(self):
        return Song.objects.all()

class UserFormView(View):
    form_class = UserForm
    template_name = 'myapp/register.html'

    def get(self,request):
        #None means we're passing nothing with the form
        form=self.form_class(None)
        return render(request,self.template_name, {'form':form})

    def post(self,request):
        form=self.form_class(request.POST)

        if form.is_valid():
            user= form.save(commit=False)

            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
        #Now we authenticate the user
            user=authenticate(username=username,password=password)
            #this will return None if user in not authenticated
            #if it returned a value
            if user is not None:
                if user.is_active:#if it's not banned/deleted ....
                    login(request,user)
                    #return redirect('myapp:index',{'user':user})
                    return render(request, 'myapp/index.html', {})
        return render(request,self.template_name, {'form':form})

def logout_request(request):
    logout(request)
    #messages.info(request, "Logged out successfully!")
    return redirect("myapp:index")

