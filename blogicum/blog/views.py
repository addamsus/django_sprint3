from django.shortcuts import render
from django.shortcuts import get_object_or_404
# from django.http import Http404
from django.utils import timezone

from .models import Category, Post

RELATED_POSTS_LEN = 5


def get_published_posts(*args, **kwargs):
    return Post.objects.select_related('category').filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
        **kwargs
    ).order_by('-pub_date')


def index(request):
    post_list = get_published_posts()[:RELATED_POSTS_LEN]
    return render(request, 'blog/index.html', context={'post_list': post_list})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post,
        pk=post_id,
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )
    return render(
        request,
        'blog/detail.html', context={'post': post}
    )


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_published_posts(
        category=category
    )
    return render(
        request,
        'blog/category.html',
        context={'post_list': post_list}
    )
