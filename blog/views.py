from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from django.db.models import Count
from .models import *
from .serializers import CommentSerializer, PostListSerializer,PostDetailSerializer
from django.shortcuts import get_object_or_404
from .filters import PostFilter
# Create your views here.




# Fetch all published posts with filtering and pagination
@api_view(['GET'])
def fetch_all_posts(request):
    post_filter = PostFilter(request.GET, queryset=Post.objects.filter(status='published'))
    posts = post_filter.qs.order_by('-created_at')

    paginator = LimitOffsetPagination()
    result_page = paginator.paginate_queryset(posts, request)

    serializer = PostListSerializer(result_page, many=True)  # Use list serializer
    return paginator.get_paginated_response(serializer.data)




# Fetch a single post with all details
@api_view(['GET'])
def fetch_single_post(request, post_id):
    post = get_object_or_404(
        Post.objects.prefetch_related('tags', 'comments').select_related('author', 'category'), id=post_id, status='published')
    serializer = PostDetailSerializer(post)
    return Response(serializer.data)




# Create a new comment for a post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    data = request.data.copy()
    data['post'] = post.id  

    serializer = CommentSerializer(data=data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, post=post) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['PATCH'])  
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure the user can only update their own comments
    if comment.user != request.user:
        return Response({'detail': 'You can only edit your own comments.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = CommentSerializer(comment, data=request.data, context={'request': request}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


