# @Date:   2019-01-08T22:36:04+06:00
# @Last modified time: 2019-01-08T23:54:19+06:00
from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    content = forms.CharField(widget = forms.Textarea(
                            attrs={
                                'class':'form-control',
                                'placeholder':"What's on your mind?",
                                'rows':3,
                                'cols':12
                            }
                        ),
                        label='',
                    )
    class Meta:
        model = Tweet
        fields = [
            'content'
        ]
