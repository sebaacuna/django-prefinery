from django.conf.urls.defaults import *
from views import signup

urlpatterns = patterns('',
        url("^signup", signup),
    )