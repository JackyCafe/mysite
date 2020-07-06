
from django.db import models
from django.contrib.auth.models import  User

# Create your models here.
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManage(models.Manager):
    def get_quesyset(self):
        return super(PublishedManage,self).get_queryset()\
            .filter(status='published')


class Post(models.Model):
    STATUS_CHOICE = (('draft','Draft'),
                     ('published','Published')
                     )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='draft')
    tags = TaggableManager()
    objects = models.Manager()
    published = PublishedManage()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return  self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'comment  by {self.name} on {self.post}'


