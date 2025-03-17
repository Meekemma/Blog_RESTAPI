from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.fetch_all_posts, name='fetch_all_posts'),
    path('post/<int:post_id>/', views.fetch_single_post, name='post'),
    path('comment/<int:post_id>/', views.create_comment, name='comment'),
    path('comment/<int:comment_id>/edit/', views.update_comment, name='update_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

]

