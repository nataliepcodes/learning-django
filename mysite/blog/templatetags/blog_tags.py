from django import template
from ..models import Post

register = template.Library()

# Retrieve total blog posts published
@register.simple_tag
def total_posts():
    return Post.published.count()