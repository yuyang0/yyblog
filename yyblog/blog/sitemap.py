#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Time-stamp: <2013-08-06 22:44:48 Tuesday by Yu Yang>

"""
the sitemap of the blog
"""
from django.contrib.sitemaps import Sitemap
from blog.models import Article

class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Article.objects.filter()

    def lastmod(self, obj):
        return obj.modified_time
