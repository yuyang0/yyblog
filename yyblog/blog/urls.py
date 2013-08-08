#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Time-stamp: <2013-08-07 21:00:27 Wednesday by Yu Yang>

"""
the URLConf of the blog app
"""
from django.conf.urls import patterns, url
from .views import RSSFeed
from .sitemap import ArticleSitemap

urlpatterns = patterns('blog.views',
    # for the home page
    url(r'^$', 'index', name='blog_index'),
    url(r'^page/(?P<page_idx>\d+)/$', 'index', name='blog_index_pages'),
    # For article page
    url(r'^article/(?P<idx>\d+)/(?P<slug>[-\w]+)/$', 'article',
        name='blog_article'),
    # For tag page
    url(r'^tag/(?P<idx>\d+)/(?P<slug>[-\w]+)/$', 'tag', name='blog_tag'),
    url(r'^tag/(?P<idx>\d+)/(?P<slug>[-\w]+)/page/(?P<page_idx>\d+)/$',
        'tag', name='blog_tag_pages'),

    url(r'^category/$', 'category_list', name='blog_category_list'),
    url(r'^category/(?P<idx>\d+)/(?P<slug>[-\w]+)/$',
        'category', name='blog_category'),
    url(r'^category/(?P<idx>\d+)/(?P<slug>[-\w]+)/page/(?P<page_idx>\d+)/$',
        'category', name='blog_category_pages'),
    # For comment
    url(r'^comment/add/$', 'ajax_add_comment', name='blog_comment'),
    # For blog search
    url(r'^search/$', 'search', name='blog_search'),
    url(r'^search/page/(?P<page_idx>\d+)/$', 'search',
        name='blog_search_pages'),
    url(r'^about/$', 'about', name='blog_about'),
    url(r'^contact/$', 'contact', name='blog_contact'),

    url(r'^ajax-upload/$', 'ajax_upload', name='blog_ajax_upload'),
    # for test
    url(r'^test/upload/$', 'test_upload'),
)

urlpatterns += patterns('',
    url(r'^rss/$', RSSFeed(), name='blog_rss'),
)

# Sitemap
sitemaps = {
    'article': ArticleSitemap,
}
urlpatterns += patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
)
