#!/usr/bin/env python
#coding=utf-8

from datetime import datetime

from django.db import models
from django.contrib.auth.admin import User
from django.conf import settings
# mptt
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from filebrowser.fields import FileBrowseField

import util


# Create your models here.
class Article(models.Model):
    """
    the model for blog article
    """
    STATUS_CHOICE = (
        (1, '编辑'),
        (2, '完成'),
        (3, '失效'),
    )
    title = models.CharField(max_length=100, verbose_name='标题')
    slug = models.SlugField(max_length=100)
    content = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modified_time = models.DateTimeField(default=datetime.now,
                                         verbose_name="修改时间")
    tags = models.ManyToManyField('Tag', blank=True,
                                  null=True, verbose_name='标签')
    category = models.ForeignKey('Category', blank=True,
                                 null=True, verbose_name='分类')
    clicks = models.IntegerField(default=0, editable=False, verbose_name='点击数')
    always_top = models.BooleanField(default=False, verbose_name='置顶')
    author = models.ForeignKey('BlogUser', verbose_name='作者')
    status = models.IntegerField(choices=STATUS_CHOICE,
                                 default=1, verbose_name='状态')

    def add_clicks(self):
        """
        update the clicks field
        """
        self.clicks += 1
        super(Article, self).save()

    @models.permalink
    def get_absolute_url(self):
        return ('blog_article', (), {'idx': self.id, 'slug': self.slug})

    def __getattr__(self, name):
        """
        add two attributes(summary, visible_comments) to the object
        Arguments:
        - `name`:
        """
        if name == 'summary':
            return util.get_summary(self.content)
        elif name == 'visible_comments':
            return self.comment_set.filter(is_visible=True)
        return super(Article, self).__getattr__(name)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-always_top', '-created_time']
        verbose_name = '博客文章'
        verbose_name_plural = '博客文章'


class Tag(models.Model):
    """
    the model of article tag
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='标签')
    slug = models.SlugField()
    # articles = models.ManyToManyField('Article', through='ArticleTag',
    #                                   verbose_name='文章')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    @models.permalink
    def get_absolute_url(self):
        return ('blog_tag', (), {'idx': self.id, 'slug': self.slug})


class Category(models.Model):
    """
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名')
    slug = models.SlugField()
    order = models.IntegerField(null=True, blank=True, verbose_name='顺序')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['order']

    @models.permalink
    def get_absolute_url(self):
        return ('blog_category', (), {'idx': self.id, 'slug': self.slug})


class Comment(MPTTModel):
    username = models.CharField(max_length=50, verbose_name='用户名')
    user_email = models.EmailField(verbose_name='邮箱地址')
    user_site = models.URLField(blank=True, verbose_name='个人网站')
    content = models.TextField(verbose_name='评论内容')
    post_time = models.DateTimeField(editable=False, default=datetime.now,
                                     verbose_name='评论时间')
    ip = models.IPAddressField(blank=True, null=True, verbose_name='IP地址')
    article_replied = models.ForeignKey('Article', blank=True, null=True,
                                        default=None, verbose_name='评论的文章')
    is_visible = models.BooleanField(default=True, verbose_name='是否可见')
    comment_replied = TreeForeignKey('self', blank=True, null=True,
                                        related_name='children')
    gravatar = models.URLField(blank=True, null=True, verbose_name='头像')

    # manger

    objects = TreeManager()

    def __getattr__(self, name):
        if name == 'is_author':
            if self.article_replied:
                author_email = self.article_replied.author.user.email
            else:
                author_email = settings.ADMINS[0][1]

            return (author_email == self.user_email)
        return super(Comment, self).__getattr__(name)

    class Meta:
        ordering = ['-post_time']
        verbose_name = '评论'
        verbose_name_plural = '评论'

    class MPTTMeta:
        parent_attr = 'comment_replied'

    def __unicode__(self):
        return self.content


class BlackList(models.Model):
    ip_address = models.IPAddressField(verbose_name='IP地址')

    class Meta:
        verbose_name = '黑名单'
        verbose_name_plural = '黑名单'

    def __unicode__(self):
        return self.ip_address


class FriendLink(models.Model):
    name = models.CharField(max_length=50, verbose_name='友情链接名称')
    url = models.URLField(verbose_name='友情链接地址')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural='友情链接'


class BlogUser(models.Model):
    """
    the model of blog user
    """
    user = models.OneToOneField(User)
    avatar = FileBrowseField(max_length=40, verbose_name='头像',
                             blank=True, null=True)
    info = models.TextField(verbose_name='用户信息')

    def __getattr__(self, name):
        if name == 'summary':
            return self.info[:400]
        elif name == 'small_avatar':
            if self.avatar:
                return self.avatar.url
            else:
                return util.get_gravatar_img_url(self.user.email)
        return super(BlogUser, self).__getattr__(name)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
