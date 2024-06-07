from django import forms
from app.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        #fields='__all__'
        fields=['username','password','email'] 
        widgets={'password':forms.PasswordInput}



class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        #fields='__all__'   if i give __all__ i will get all the values which are present in user
        fields=['address','profile']
              