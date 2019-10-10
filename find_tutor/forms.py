from django import forms
from django.contrib.auth.models import User
from .models import Register

class UserForm(forms.Form):
    firstname = forms.CharField(max_length=30,required=True)
    lastname= forms.CharField(max_length=30,required=True)
    email = forms.EmailField(max_length=100,required=True,help_text="Required Inform a valid email address")
    #password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        field = ('username','first_name','last_name','email','password1','password2')

