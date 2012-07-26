from django import template
from django.conf import settings
from hashlib import sha1

register = template.Library()

@register.simple_tag
def tester_hash(email):
    return sha1("%s%s" % (settings.PREFINERY_BETA_DECODER_KEY, email)).hexdigest()

@register.simple_tag
def prefinery_subdomain():
    return settings.PREFINERY_SUBDOMAIN

@register.simple_tag
def prefinery_beta_id():
    return settings.PREFINERY_BETA_ID