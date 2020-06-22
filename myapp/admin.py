from django.contrib import admin
from myapp.models import Song
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.

admin.site.register(Song)

TokenAdmin.raw_id_fields = ['user']
