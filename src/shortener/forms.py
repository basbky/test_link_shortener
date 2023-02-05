from django import forms
from django.forms import URLInput


class URLShortenerForm(forms.Form):
    url = forms.URLField(
        label='',
        error_messages={'required': 'Введите корректную ссылку'},
        widget=forms.URLInput(
            attrs={
                'class': 'form-field',
                'placeholder': 'https://example.com/',
            }
        ),
    )
