#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Time-stamp: <2013-08-04 14:13:53 Sunday by Yu Yang>

"""
admin for blog app
"""
from django.contrib import admin
from models import Article, Category, Tag, Comment, BlackList, \
    FriendLink, BlogUser

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
                    'created_time', 'modified_time', 'slug', 'author')
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, MPTTModelAdmin)

admin.site.register(BlackList)
admin.site.register(FriendLink, FriendLinkAdmin)
admin.site.register(BlogUser)


# admin.site.register(Subscriber, SubscriberAdmin)
