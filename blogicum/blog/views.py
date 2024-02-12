from django.shortcuts import render
from django.http import Http404
from django.utils import timezone
from datetime import datetime

from .models import Category, Post


def index(request):
    template_name = 'blog/index.html'
    post_list = Post.objects.select_related('category').filter(
        is_published=True,
        pub_date__lte=datetime.now(),
        category__is_published=True,
    ).order_by('-pub_date')[:5]
    return render(request, template_name, context={'post_list': post_list})


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
        pub_date__lte=datetime.now(),
        category__slug=category_slug,
    )
    return render(request, template_name, context={'post_list': post_list})
