import django_filters
from api.models import Post

class PostTopicFilter(django_filters.FilterSet):
    topic = django_filters.CharFilter(field_name="topic",lookup_expr="icontains")
    
    class Meta:
        model = Post
        fields = ['topic']