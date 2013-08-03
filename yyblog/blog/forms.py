#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Time-stamp: <2013-08-03 14:04:15 Saturday by Yu Yang>

"""
comment form
"""
from django import forms

from models import Comment, Article

class CommentForm(forms.ModelForm):
    """
    comment form
    """
    # username = forms.CharField()
    # user_email = forms.EmailField()
    # user_site = forms.URLField(required=False)
    # content = forms.CharField(widget=forms.Textarea())
    username = forms.CharField(
                    widget=forms.TextInput)
    user_email = forms.EmailField(
                    widget=forms.TextInput)
    user_site = forms.URLField(
                    widget=forms.TextInput, required=False, max_length=200)
    content = forms.CharField(widget=forms.Textarea)

    # Hidden field
    article_replied = forms.ModelChoiceField(Article.objects.all(),
                                             widget=forms.HiddenInput,
                                             required=False)
    comment_replied = forms.ModelChoiceField(Comment.objects.all(),
                                        widget=forms.HiddenInput,
                                        required=False)

    class Meta:
        model = Comment
