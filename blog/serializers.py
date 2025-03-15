from rest_framework import serializers
from blog.models import Category, Tag, Post, Comment
from datetime import timedelta
from django.utils import timezone



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = ['id', 'name']




class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'body', 'created_at']


class PostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)  # Fixed related name

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'image', 'comment_count', 'category', 'tags', 'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='get_author_full_name', read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)  # Fixed related name
    related_posts = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'image', 'category', 'tags', 'content', 'comments', 'related_posts', 'created_at', 'updated_at']

    def get_related_posts(self, obj):
        """
        Fetch related posts based on the same category, excluding the current post.
        """
        related = Post.objects.filter(category=obj.category, status='published').exclude(id=obj.id).order_by('-created_at')[:5]  # Latest related posts
        return PostListSerializer(related, many=True).data






    

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'body', 'created_at']

    def get_user(self, obj):
        """
        Retrieve the full name of the user who made the comment.
        """
        return obj.user.get_full_name()
    

    def validate_post(self, value):
        """
        Check if the post is published before allowing comments.
        """
        if value.status != 'published':
            raise serializers.ValidationError("You can only comment on published posts.")
        return value
    


    def validate_body(self, value):
        """
        Check if the comment is empty.
        """
        if not value:
            raise serializers.ValidationError("Comment body cannot be empty.")

        if len(value) > 200:
            raise serializers.ValidationError("Comment body cannot exceed 200 characters.")
        return value
    


    def create(self, validated_data):
        """
        Create a new comment instance.
        """
        post = validated_data.pop('post')
        user = self.context['request'].user

        validated_data.pop('user', None)

        comment = Comment.objects.create(post=post, user=user, **validated_data)

        return comment

    def update(self, instance, validated_data):
        """
        Update an existing comment instance.
        """
        request = self.context['request']
        user = request.user

        if instance.user != user:
            raise serializers.ValidationError("You are not allowed to update this comment.")

        # Check if the comment was made within the last 5 minutes
        time_elapsed = timezone.now() - instance.created_at

        if time_elapsed > timedelta(minutes=5):  # Fixed typo
            raise serializers.ValidationError("You can only update your comment within 5 minutes.")

        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance
