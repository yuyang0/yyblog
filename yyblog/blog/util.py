#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Time-stamp: <2013-08-06 12:04:36 Tuesday by Yu Yang>

"""
some useful function for blog app
"""
import urllib
import urllib2
import os
import hashlib
import random
import string


def get_summary(html):
    """
    get summary of html string
    """
    MAX_LINES = 40
    lines = html.split(os.linesep)
    results = lines[:MAX_LINES]
    return ''.join(results)


def get_user_IP(request):
    """
    get client ip address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        return ip


def get_theme(request):
    """
    get theme from cookie
    Arguments:
    - `request`:the HTTPRequest instance
    """
    theme = request.COOKIES.get('theme', 'dopetrope')
    if theme not in ('dopetrope', 'striped', 'azsands'):
        theme = 'dopetrope'
    return theme


def get_gravatar_img_url(email, size=40,
                         default=''):
    """
    get the url of image stored in gravatar
    Arguments:
    - `email`:
    - `size`:the size of image you want to get
    """
    # construct the url
    gravatar_url = "http://www.gravatar.com/avatar/" + \
                   hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':'404', 's':str(size)})
    try:
        urllib2.urlopen(gravatar_url)
    except urllib2.URLError:
        gravatar_url = default
    return gravatar_url


def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    """
    """
    return ''.join(random.choice(chars) for x in range(size))


if __name__ == '__main__':
    # print get_gravatar_img_url('yy2012cn@gmail.com')
    print random_string()
