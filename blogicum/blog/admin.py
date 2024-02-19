from django.contrib import admin

from .models import Category, Location, Post


class PostAdmin (admin.ModelAdmin):
    list_display = [
        'title',
        'pub_date',
        'text',
        'author',
        'location',
        'category',
        'is_published'
    ]
    list_filter = ['is_published']
    search_fields = ['title']


admin.site.register(Category)
admin.site.register(Location)


admin.site.register(Post, PostAdmin)
