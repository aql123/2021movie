import hashlib
from urllib.parse import urlencode

from django import template

register = template.Library()


# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|gravatar:150 }}
@register.filter
def gravatar(email, size="75"):
    """
    <img src='{{ request.user.email|gravatar:"75" }}'>
    """
    gravatar_url = "//www.gravatar.com/avatar/" + \
                   hashlib.md5(email.encode('utf-8')).hexdigest() + "?"
    gravatar_url += urlencode({'d': 'retro', 's': str(size)})
    return gravatar_url
