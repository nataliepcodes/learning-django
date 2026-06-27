from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail

# A view to retrieve all published posts
def post_list(request):
    object_list = Post.published.all()
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
                   'posts': posts})


# A view to display a single post
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day) # "use the day component of the publish field"
    return render(request, 
                  'blog/post/detail.html',
                  {'post': post})

# A view to share a post by email
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid:
            # Form fields passed validation
            cd = form.cleaned_data
            # Send email
            post_url = request.build_absolute_url(post.get_absolute_url)
            subject = f"{cd['name']}recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@blog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})