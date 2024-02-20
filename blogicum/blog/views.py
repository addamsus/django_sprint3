from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

RELATED_POSTS_LEN = 5


def get_published_posts(*args, **kwargs):
    return Post.objects.select_related(
        'category',
        'author',
        'location'
    ).filter(
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
        get_published_posts(),
        pk=post_id,
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
