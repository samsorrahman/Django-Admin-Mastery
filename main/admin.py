from typing import Any, List, Tuple, Union
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Blog
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created', 'last_modified', 'is_draft']
    list_filter = ['is_draft']
    search_fields = ['title']
    def get_ordering(self, request):
        if request.user.is_superuser:
            return ('title', '-date_created')
        
        return ('title')
    
    
admin.site.register(Blog, BlogAdmin)