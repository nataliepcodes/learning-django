from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()

# Retrieve total blog posts published / Displayed on the blog sidebar
@register.simple_tag
def total_posts():
    return Post.published.count()

# Display latest posts / Displayed on the blog sidebar
"""
How it works:
0. There are 2 html templates (base.html and latest_posts.html) and 1 py file (blog_tags.py)
1. Django will call latest posts show_latest_posts() in blog_tags.py, the data is asked from base.html that is asking for 3 latests posts - {% show_latest_posts 3 %}
2. show_latest_posts() in the below function will get the latest posts from the Post class and will return/output the data 
3. The return data will be used in latest_posts.html that is registered in the inclusion tag of show_latest_posts()
4. latest_posts.html has a loop that iterates over a dictionary of values
5. What's a link between base.html and latest_posts.html? 
- {% show_latest_posts 3 %} in base.html is a shortcut to include another template, in this case latest_posts.html which is inluded at the registration step of show_latest_posts()
- the show_latest_posts() return data is first processed within the loop in latest_posts.html, then the final result is displayed in the base.html
"""
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts' : latest_posts} 

# A tag to display the most commented post
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]