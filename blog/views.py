from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import EmailPostForm, CommentForm
from .models import Post,Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import  Count
import logging as log


# Create your views here.
def index(request):
    return HttpResponse('媽～我在這裡'               )


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    comments: Comment
    new_comment :Comment
    comment_form :CommentForm
    new_comment=None
    post = get_object_or_404(Post, slug=post,
                             publish__year=year,
                             publish__month = month
                              )
    comments = post.comments.filter(active=True)
    if request.method =='POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request, 'blog/post/post_detail.html',
                  {'post': post,'comments':comments,
                   'new_comment':new_comment,
                   'comment_form':comment_form,
                   'similar_posts':similar_posts
                   })


def post_share(request,post_id):
    form :EmailPostForm
    post = get_object_or_404(Post,id = post_id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} 推薦您  {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, cd['email'], [cd['to']])
            sent = True

    else:
        form = EmailPostForm()

    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})