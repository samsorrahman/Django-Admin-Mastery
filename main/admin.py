from rangefilter.filters import  DateRangeFilterBuilder
from django_admin_listfilter_dropdown.filters import  RelatedDropdownFilter
from django.contrib import admin
from django.db.models import Count
from .models import Blog, Comment, Category
from django.contrib import messages
from django.utils import timezone
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class CommentInline(admin.TabularInline):
    model= Comment
    fields = ('text', 'is_active')
    extra= 1
    classes = ('collapse',)
    
    

class BlogAdmin(SummernoteModelAdmin):
    list_display = ['title', 'date_created', 'last_modified', 'is_draft', 'days_since_creation', 'no_of_comments']
    list_filter = (
        "is_draft",
        ("date_created", DateRangeFilterBuilder()),
    )
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20
    actions = ('set_blogs_to_published',)
    date_hierarchy = ('date_created')
    inlines = [CommentInline]
    filter_horizontal = ('categories',)
    fieldsets = (
    (None, {
        'fields': (('title', 'slug'), 'body'),
    }),
    ('Advance Options', {
        'fields': ('is_draft', 'categories' ),
        'description': 'Option to configure blog creation',
        'classes': ('collapse',)
    }),
    )
    summernote_fields = ('body',)
    
    def get_queryset(self, request):
        queryset= super().get_queryset(request)
        queryset= queryset.annotate(comments_count=Count('comments'))
        return queryset
    
    def no_of_comments(self, blog):
        return blog.comments_count
    no_of_comments.admin_order_field= 'comments_count'
    def get_ordering(self, request):
        if request.user.is_superuser:
            return ('title', '-date_created')
        
        return ('title')
    
    def days_since_creation(self,blog):
        diff= timezone.now() - blog.date_created
        return diff.days
    days_since_creation.short_description = 'Days active'
    
    
    def set_blogs_to_published(self, request, queryset):
        count = queryset.update(is_draft=False)
        self.message_user(request, '{} blogs have been published successfully.'.format(count), messages.SUCCESS)
    set_blogs_to_published.short_description= 'Mark selected blog as published'
    
    
class CommentAdmin(admin.ModelAdmin):
    list_display =('blog','text', 'date_created', 'is_active')
    list_editable = ('text', 'is_active',)
    list_per_page = 10
    list_filter = (
        ('blog', RelatedDropdownFilter),
    )
    
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)