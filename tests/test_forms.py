import pytest

from shortener.forms import URLShortenerForm


@pytest.mark.django_db
def test_url_shortener_form():
    # Проверяет форму на валидность при пустом поле
    form = URLShortenerForm({'url': ''})
    assert form.is_valid() is False

    # Проверяет корректность error message
    assert 'url' in form.errors
    assert form.errors['url'] == ['Введите корректную ссылку']

    # Проверяет форму на валидность при заведомо корректных вводных данных
    form = URLShortenerForm({'url': 'https://www.example.com'})
    assert form.is_valid() is True

    # Проверяет форму на возврат url при заведомо верном url
    assert form.cleaned_data.get('url') == 'https://www.example.com'
