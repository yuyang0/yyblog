#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Time-stamp: <2013-08-02 13:27:54 Friday by Yu Yang>

"""
admin for blog app
"""
from django.contrib import admin
from models import Article, Category, Tag, Comment

from django.db import models
# from epiceditor.widgets import AdminEpicEditorWidget
from pagedown.widgets import AdminPagedownWidget
from mptt.admin import MPTTModelAdmin

# class ArticleAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.TextField: {'widget': AdminEpicEditorWidget },
#     }
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'always_top', 'status', 'clicks',
                    'created_time', 'modified_time', 'slug')
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment, MPTTModelAdmin)
# admin.site.register(BlogUser)
# admin.site.register(Link, LinkAdmin)
# admin.site.register(BlackList)
# admin.site.register(Subscriber, SubscriberAdmin)
