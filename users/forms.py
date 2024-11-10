from django import forms
from django.contrib.auth.models import User


class SignupPage(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder' : 'Username'}),
        label=''
        )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder' : 'Email'}),
        label=''
        
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}),
        required=True,
        label=''
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm Password'}),
        required=True,
        label=''
    )



    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError ('Passwords do not match')
        
        return cleaned_data
    

class LoginPage(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder' : 'Username'}),
        label=''
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}),
        required=True,
        label=''
    )
