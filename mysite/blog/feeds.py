from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):
    # 'title', 'link', 'description' correspond to RSS feed
    title = 'My blog'
    # Generate url for the link attribute
    link = reverse_lazy('blog:post_list')
    description = 'New post of my blog.'

    # Retrieve the objects to be included in the feed - last 5 published posts
    def items(self):
        return Post.published.all()[:5]
    
    # Retrieve blog title
    def item_title(self, item):
        return item.title
    
    # Retrieve blog description
    def item_description(self, item):
        return truncatewords(item.body, 30) # builds post description with the first 30 words