#!/usr/bin/env python
#coding=utf8

# Create your views here.
import os
import os.path
import json
import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import get_template
from django.template import Context, RequestContext

from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import F
from django.core.context_processors import csrf
from django.contrib.auth.admin import User
# Rss
from django.contrib.syndication.views import Feed

from .models import Article, Tag, Category, Comment, BlackList, FriendLink
from forms import CommentForm
import util
from .search import get_query

PAGE_SIZE = 5
RANGE_NUM = 5

def paginator_response(max_idx, current_idx, entry_num):
    """
    response of paginator
    """
    range_start = (current_idx//RANGE_NUM) * RANGE_NUM  + 1
    range_end = range_start + RANGE_NUM
    if range_end >= max_idx:
        range_end = max_idx + 1
        min_start = range_end - RANGE_NUM
        if min_start <= 0:
            min_start = 1
        range_start = min(range_start, current_idx, min_start)
    else:
        range_start = min(range_start, current_idx)
    center_range = range(range_start, range_end)

    show_first = False if range_start == 1 else True
    show_last = False if range_end > max_idx else True
    show_previous = False if current_idx == 1 else True
    show_next = False if current_idx == max_idx else True

    entry_start_idx = (current_idx - 1) * PAGE_SIZE + 1
    entry_end_idx = current_idx * PAGE_SIZE
    entry_end_idx = entry_num if entry_num < entry_end_idx else entry_end_idx
    ret = {
        'center_range': center_range,
        'show_first': show_first,
        'show_last': show_last,
        'show_previous': show_previous,
        'show_next': show_next,
        'max_idx': max_idx,
        'current_idx': current_idx,

        # Fixme: test max_idx
        'start': entry_start_idx,
        'end': entry_end_idx,
    }
    return ret


def get_common_resp_ctx():
    '''
    get the dict for context,mainly used to render sidebar.html
    '''
    recent_comments = Comment.objects.filter(is_visible=True).\
                      order_by('-post_time')[:5]
    common_ctx = {
        'populars': Article.objects.order_by('-clicks')[:5],
        'tags': Tag.objects.all(),
        'categories': Category.objects.all(),
        'recent_comments': recent_comments,
        'links': FriendLink.objects.all(),
        'site_title': settings.SITE_TITLE,
    }
    # Get Administrator of this site
    common_ctx['author'] = User.objects.get(username='admin').bloguser
    return common_ctx


def page_index_common_resp_ctx(page_idx, objs):
    """
    只要是有分页代码的页面都由这个函数设计负责处理，比如home，tag，category
    """
    idx = int(page_idx)
    p = Paginator(objs, PAGE_SIZE)
    try:
        articles = p.page(idx)
    except (EmptyPage,InvalidPage):
        # articles = p.page(p.num_pages)
        raise Http404
    ctx = {'articles': articles}
    ctx.update(paginator_response(p.num_pages, idx, len(objs)))

    ctx.update(get_common_resp_ctx())

    return ctx


def index(request, page_idx=1):
    ctx = page_index_common_resp_ctx(page_idx, Article.objects.all())
    url_prefix = reverse('blog_index')
    ctx['url_prefix'] = url_prefix

    theme = util.get_theme(request)
    return render_to_response('blog/%s/%s' % (theme, 'index.html'), ctx)


def article(request, idx, slug):
    """
    the view generate article page
    Arguments:
    - `idx`:the primary key field in the database
    - `slug`: the slug field
    """
    theme = util.get_theme(request)
    idx = int(idx)
    article = get_object_or_404(Article, pk=idx)
    ctx = {
        'article': article,
    }
    # comments
    nodes = article.comment_set.filter(is_visible=True)
    nodes = list(nodes)
    ctx['nodes'] = nodes

    ctx.update(get_common_resp_ctx())
    ctx.update(csrf(request))
    ctx['form'] = CommentForm()
    # Update clicks field
    article.clicks = F('clicks') + 1
    article.save(update_fields=['clicks'])

    return render_to_response('blog/%s/article.html' % theme, ctx)


def tag(request, idx, slug, page_idx=1):
    """
    """
    t = Tag.objects.get(pk=int(idx))
    articles = t.article_set.all()

    ctx = page_index_common_resp_ctx(page_idx, articles)
    # url_prefix = reverse('blog_tag', args=(idx, slug))
    # ctx['url_prefix'] = url_prefix
    ctx.update({'idx': idx, 'slug': slug})
    ctx['tag'] = t

    theme = util.get_theme(request)
    return render_to_response('blog/%s/%s' % (theme, 'tag.html'), ctx)


def category_list(request):
    categories_with_articles = Category.objects.all()
    for category in categories_with_articles:
        category.articles = category.article_set.all()[:5]

    data = locals()
    data.update(get_common_resp_ctx())

    theme = util.get_theme(request)
    return render_to_response('blog/%s/categories.html' % theme, data)


def category(request, idx, slug, page_idx=1):
    """
    """
    cate = Category.objects.get(pk=int(idx))
    articles = cate.article_set.all()

    ctx = page_index_common_resp_ctx(page_idx, articles)
    # url_prefix = reverse('blog_category', args=(idx, slug))
    # ctx['url_prefix'] = url_prefix
    ctx.update({'idx': idx, 'slug': slug})

    ctx['category'] = cate

    theme = util.get_theme(request)
    return render_to_response('blog/%s/%s' % (theme, 'category.html'), ctx)


def ajax_add_comment(request):
    '''
    using ajax to add comment
    '''
    if request.method == 'POST':
        f = CommentForm(request.POST)
        if f.is_valid():
            comment = f.save(commit=False)

            comment.ip = util.get_user_IP(request)
            # test if the ip address is in black list
            if BlackList.objects.filter(ip_address=comment.ip):
                d = {
                    'success': False,
                    'msg': '评论失败，你的ip被屏蔽'
                }
                return HttpResponse(json.dumps(d))

            comment.user_email = comment.user_email.strip()
            comment.gravatar = util.get_gravatar_img_url(
                comment.user_email,
                default='/static/img/gravatar.jpg'
            )
            comment.is_visible = True
            comment.save()

            article_id = comment.article_replied
            nodes = Comment.objects.filter(article_replied=article_id,
                                           is_visible=True)

            nodes = list(nodes)

            theme = util.get_theme(request)
            ctx = {'nodes': nodes}
            t = get_template('blog/%s/comments.html' % theme)
            html = t.render(Context(ctx))
            d = {
                'html': html,
                'id': comment.id,
                'success': True,
                'msg': '评论成功，正在更新评论列表'
            }
            json_data = json.dumps(d)
        else:
            d = {'success': False, 'msg': '评论失败，数据填写不正确!'}
            json_data = json.dumps(d)
    else:
        d = {
            'success': False,
            'msg': '评论失败，非POST请求'
        }
        json_data = json.dumps(d)
    return HttpResponse(json_data)


def search(request, page_idx=1):
    theme = util.get_theme(request)

    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'content',])

        found_entries = Article.objects.filter(entry_query)
        # ctx = {
        #     'query_string': query_string,
        #     'results': found_entries
        # }
        ctx = page_index_common_resp_ctx(page_idx, found_entries)

    return render_to_response('blog/%s/search.html' % theme, ctx,
                              context_instance=RequestContext(request))


def ajax_upload(request):
    """
    view of ajax file upload
    """
    files = request.FILES.values()
    if not files:
        d = {
            'success': False,
            'msg': '文件上传失败，文件栏为空！'
        }
        return HttpResponse(json.dumps(d))
    f = files[0]

    ext = os.path.splitext(f.name)[1]
    now = datetime.datetime.now()
    directory = os.path.join(settings.MEDIA_ROOT, repr(now.year),
                             '%02d' % now.month)
    # Create directory if it didn't  exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = '%02d-%02d-%02d-%06d_%s' %(now.hour, now.minute, now.second,
                                          now.microsecond, util.random_string())
    filename += ext
    dest_file = os.path.join(directory, filename)
    file_url = os.path.join(settings.MEDIA_URL,
                            dest_file[len(settings.MEDIA_ROOT):])
    with open(dest_file, 'wb') as fp:
        for chunk in f.chunks():
            fp.write(chunk)

    d = {
        'success': True,
        'msg': '文件上传成功！',
        'url': file_url
    }
    return HttpResponse(json.dumps(d))


def about(request):
    """

    Arguments:
    - `request`:
    """
    ctx = get_common_resp_ctx()
    theme = util.get_theme(request)
    return render_to_response('blog/%s/about.html' % theme, ctx)


def contact(request):
    theme = util.get_theme(request)
    ctx = get_common_resp_ctx()

    ctx.update(csrf(request))

    nodes = Comment.objects.filter(article_replied=None, is_visible=True)
    nodes = list(nodes)
    ctx['nodes'] = nodes

    ctx['form'] = CommentForm()
    return render_to_response('blog/%s/contact.html' % theme, ctx)


class RSSFeed(Feed):
    title = u"残阳似血的博客"
    description = "Lost good things..."
    link = "/"

    def items(self):
        return Article.objects.all().order_by("-created_time")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary

# for test
def test_upload(request):
    ctx = {}
    ctx.update(csrf(request))
    return render_to_response('blog/dopetrope/test_uploader.html', ctx)
