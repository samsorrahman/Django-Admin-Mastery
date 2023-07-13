from typing import Any, List, Tuple, Union
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Blog
from django.contrib import messages
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created', 'last_modified', 'is_draft']
    list_filter = ['is_draft', 'date_created']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20
    actions = ('set_blogs_to_published',)
    
    def get_ordering(self, request):
        if request.user.is_superuser:
            return ('title', '-date_created')
        
        return ('title')
    
    def set_blogs_to_published(self, request, queryset):
        count = queryset.update(is_draft=False)
        self.message_user(request, '{} blogs have been published successfully.'.format(count), messages.SUCCESS)
    set_blogs_to_published.short_description= 'Mark selected blog as published'
    
admin.site.register(Blog, BlogAdmin)