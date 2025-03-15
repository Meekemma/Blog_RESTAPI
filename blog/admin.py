from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE  
from .models import Post, Category, Tag, Comment


class PostForm(forms.ModelForm):
    """Custom form to use TinyMCE for the content field."""
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('title', 'author', 'get_status', 'created_at', 'updated_at')  
    list_filter = ('status', 'created_at', 'author', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)  
    filter_horizontal = ('tags',)

    def get_status(self, obj):
        return obj.get_status_display()  # Convert choice field to readable format
    get_status.short_description = 'Status'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'active', 'created_at')  
    list_filter = ('active', 'created_at', 'post')
    search_fields = ('body', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
