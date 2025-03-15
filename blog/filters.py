from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Post

class PostFilter(filters.FilterSet):
    q = filters.CharFilter(method='filter_search')

    class Meta:
        model = Post
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(category__name__icontains=value) | 
            Q(tags__name__icontains=value)
        ).distinct().order_by('-created_at') 
