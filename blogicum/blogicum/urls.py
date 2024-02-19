from django.contrib import admin
from django.urls import path
from django.urls import include

app_name = 'blogicum'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls')),
    path('', include('blog.urls')),
]
