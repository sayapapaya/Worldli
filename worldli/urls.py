from django.conf.urls import patterns, include, url
from django.contrib import admin
from app import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'worldli.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name="index"),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^profile/', views.profile, name="profile"),
    url(r'^create_user/', views.create_user, name="create_user"),
    url(r'^admin/', include(admin.site.urls)),
)
