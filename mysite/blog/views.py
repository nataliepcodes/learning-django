from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


# A view to retrieve all published posts
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # __in field lookup; many-to-many relationship - one post can have multiple tags, multiple tags can related to multiple posts
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list,3) # 3 posts on each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver the last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',
                  {'page': page, 
                   'posts': posts,
                   'tag': tag,})


# A view to display a single post
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day) # "use the day component of the publish field"
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment (many-to-one: many comments-one post)
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    # List of similar posts
    # Get post tags by id (flat=True turns tuple single values into a list of integers)
    post_tags_ids = post.tags.values_list('id', flat=True)
    # Get posts that include similar tags excluding current post
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # Order posts with same tags in descending order by published date, and display the recent 4 posts
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


# A view to share a post by email
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # Send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@blog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


# Text Search View
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            # Create search query object
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            # Filter results by SearchQuery, use SearchRank to order results. Order by relevancy
            results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector,search_query)).filter(search=search_query).order_by('-rank')

    return render(request, 'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})        

