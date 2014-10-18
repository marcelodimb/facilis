from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/admin')),
    url(r'^admin/', include(admin.site.urls)),
)
