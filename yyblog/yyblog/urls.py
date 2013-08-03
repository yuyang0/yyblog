from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yyblog.views.home', name='home'),
    # url(r'^yyblog/', include('yyblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Grappelli url mapping
urlpatterns += patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    # (r'^admin/filebrowser/', include(site.urls)),
)

urlpatterns += patterns('',
	url(r'^', include('blog.urls')),
)

# Static files url if DEBUG
urlpatterns += staticfiles_urlpatterns()
# User upload files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
