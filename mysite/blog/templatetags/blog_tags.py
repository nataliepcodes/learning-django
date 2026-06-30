from django import template
from ..models import Post

register = template.Library()

# Retrieve total blog posts published / Displayed on the blog sidebar
@register.simple_tag
def total_posts():
    return Post.published.count()

# Display latest posts / Displayed on the blog sidebar
@register.inclusion_tag('blog/post/latest)posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts' : latest_posts}