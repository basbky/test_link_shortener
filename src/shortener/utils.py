import random
import string

from .models import Link


def generate_short_hash(length=6):
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )


def save_url_mapping(url):
    while True:
        short_hash = generate_short_hash()
        if not Link.objects.filter(short_hash=short_hash).exists():
            break
    Link.objects.create(original_url=url, short_hash=short_hash)
    return short_hash
