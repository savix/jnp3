from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
#    (r'^async-test-list$', 'jnp3.photos.views.async_test_list'),
#    (r'^async-test-add$', 'jnp3.photos.views.async_test_add'),
    (r'^$', 'jnp3.views.home'),
    (r'^login$', 'jnp3.views.login'),
    (r'^logout$', 'jnp3.views.logout'),
    (r'^register$', 'jnp3.views.register'),
    (r'^upload$', 'jnp3.photos.views.upload'),
    (r'^search$', 'jnp3.photos.views.search'),
    (r'^gallery/(?P<username>\w+)/(?P<page>1\d*)$', 'jnp3.photos.views.gallery'),
    (r'^photo/(?P<id>\d+)$', 'jnp3.photos.views.photo'),
    # Examples:
    # url(r'^$', 'jnp3.views.home', name='home'),
    # url(r'^jnp3/', include('jnp3.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
