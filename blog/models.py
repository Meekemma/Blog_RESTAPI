from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model


User = get_user_model()



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True) 

    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True) 

    def __str__(self):
        return self.name



STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

class Post(models.Model):
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True)
    content = HTMLField()
    image = models.ImageField(
        upload_to='image/posts/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')  
    tags = models.ManyToManyField(Tag, related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_published = models.BooleanField(default=False, db_index=True)  
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  

    def get_author_full_name(self):
        return f"{self.author.first_name} {self.author.last_name}"

    def __str__(self):
        return self.title




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    body = models.TextField()
    active = models.BooleanField(default=True, db_index=True)  
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return f'Comment by {self.user.email} on {self.post}'
    
    def get_user_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
