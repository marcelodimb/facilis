from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from sap import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/admin')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^set_auditor_responsavel/', views.set_auditor_responsavel),
)
