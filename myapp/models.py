from django.db import models
from django.urls import reverse
# Create your models here.

class Song(models.Model):
    name = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)
    album = models.CharField(max_length=100,default='',null=False)
    isFavorite= models.BooleanField(default=False)
    logo= models.FileField(blank=True, null=True)


    def __str__(self):
        return self.name + '-' + self.album

    def get_absolute_url(self):
        return reverse('myapp:song', kwargs= {'pk' : self.pk} )

