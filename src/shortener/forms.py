from django import forms
from django.forms import URLInput


class URLShortenerForm(forms.Form):
    """
    Форма для принятия полной ссылки и последующего сокращения
    """

    # URLField принимает URL от пользователя
    url = forms.URLField(
        label='',
        # Кастомные error messages
        error_messages={'required': 'Введите корректную ссылку'},
        # URLInput widget to render the form field
        widget=forms.URLInput(
            attrs={
                'class': 'form-field',
                # Образец для ввода ссылки
                'placeholder': 'https://example.com/',
            }
        ),
    )
