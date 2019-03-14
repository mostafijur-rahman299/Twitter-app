# @Date:   2019-03-11T12:36:31+06:00
# @Last modified time: 2019-03-13T00:26:41+06:00
import string
from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo

class UserForm(forms.ModelForm):
    username = forms.CharField(widget = forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Display name'
                                    }
                                )
                            )
    email = forms.EmailField(widget=forms.EmailInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Example@gmail.com'
                                    }
                                )
                            )
    password = forms.CharField(widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Password'
                                    }
                                )
                            )
    password2 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Confirm Password'
                                    }
                                )
                            )

    class Meta():
        model=User
        fields=('username','email','password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('Username is taken!')
        return username
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Password must match!')
        if len(password) < 6:
            raise forms.ValidationError('Password length 6 or up!')
        a = False
        for _ in password:
            if _ in string.ascii_lowercase:
                a = True
        if a == False:
            raise forms.ValidationError('Password at least one charecter!')
        return data

class UserProfileInfoForm(forms.ModelForm):
    portfolio_site = forms.URLField(widget=forms.URLInput(
                                            attrs={
                                                'class': 'form-control',
                                                'placeholder': 'https://www.example.com'
                                            }
                                        )
                                    )
    class Meta():
        model=UserProfileInfo
        fields=('portfolio_site','profile_pic')

class LoginForm(forms.Form):
    username   = forms.CharField(widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Username'
                                        }
                                    )
                                )
    password   = forms.CharField(widget=forms.PasswordInput(
                                        attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Password'
                                        }
                                    )
                                )
