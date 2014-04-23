from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'upload/','queries.views.upload_file'),
)