from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
