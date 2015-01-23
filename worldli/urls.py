from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib import admin
from app import views
import settings


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'worldli.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name="index"),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^profile/', views.profile, name="profile"),
    url(r'^create_user/', views.create_user, name="create_user"),
    url(r'^create_post/', views.create_post, name="create_post"),
    url(r'^create_problem/', views.create_problem, name="create_problem"),
    url(r'^upload_images/(?P<problem_id>\d+)/$', views.upload_images, name="upload_images"),
    url(r'^delete_image/(?P<image_id>\d+)$', views.delete_image, name="delete_image"),
    url(r'^post/(?P<problem_id>\d+)$', views.view_post, name="view_post"),
    url(r'^place_autocomplete/', views.place_autocomplete, name="place_autocomplete"),
    url(r'^my_post/', views.my_post, name="my_post"),
    url(r'^edit_post/(?P<problem_id>\d+)$', views.edit_post, name="edit_post"),
    url(r'^edit_problem/(?P<problem_id>\d+)$', views.edit_problem, name="edit_problem"),
    url(r'^delete_problem/(?P<problem_id>\d+)$', views.delete_problem, name="delete_problem"),
    url(r'^search_autocomplete/', views.search_autocomplete, name="search_autocomplete"),
    url(r'^search/', views.search, name="search"),
    url(r'^search_people_name/', views.search_people_name, name="search_people_name"),
    url(r'^search_skills/', views.search_skills, name="search_skills"),
    url(r'^create_comment/(?P<problem_id>\d+)$', views.create_comment, name="create_comment"),
    url(r'^delete_comment/(?P<comment_id>\d+)$', views.delete_comment, name="delete_comment"),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))

urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)
