from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render,redirect


#registration form
class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']

#login Form
class LoginForm(forms.Form):

    username = forms.CharField(max_length=254,)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password']
