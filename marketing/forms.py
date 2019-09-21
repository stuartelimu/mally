from django import forms
from .models import NewsLetter

class EmailSignupForm(forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields = ('email',)
        