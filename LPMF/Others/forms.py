from django import forms
from django.db.models import fields
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  ,UserChangeForm
from .models import Category


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

# class UserProfileForm(forms.ModelForm):
    
#     class Meta:
#         model = UserProfile
#         field = "__all__"
#         exclude = ['userprofile_uid']

class EditUserProfileForm(UserChangeForm):
    
    password = None
    class Meta:
        model = User
        fields= ['username','first_name','last_name','email','date_joined','last_login']
        labels = {'email':'Email'}

class EditAdminProfileForm(UserChangeForm):
    
    password = None
    class Meta:
        model = User
        fields= '__all__'
    

class CategoryDisplayForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = "__all__"