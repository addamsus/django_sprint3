from django.shortcuts import render
from django.http import Http404
from django.utils import timezone

from .models import Category, Post

RELATED_POSTS_LEN = 5

def index(request):
    post_list = Post.objects.select_related(
        'category',
        'author',
        'location'
        ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    ).order_by('-pub_date')[:RELATED_POSTS_LEN]
    return render(request, 'blog/index.html', context={'post_list': post_list})


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    try:
        post = Post.objects.select_related('category').get(id=post_id)
    except Post.DoesNotExist:
        raise Http404('Такого поста не существует.')
    if (
        post.pub_date > timezone.now()
        or not post.is_published
        or not post.category.is_published
    ):
        raise Http404('Пост не найден.')
    return render(
        request,
        template_name, context={'post': post}
    )


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    if not Category.objects.get(slug=category_slug).is_published:
        raise Http404('Категория не найдена.')
    post_list = Post.objects.select_related('category').filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__slug=category_slug,
    )
    return render(request, template_name, context={'post_list': post_list})
