import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

STATUS = (
    (0, 'Drafted'),
    (1, 'Public')
)


class Post(models.Model):
    slug = models.SlugField(max_length=200, unique=True, default=uuid.uuid1)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=2000, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    # photo = models.ImageField(upload_to='gallery')
    status = models.IntegerField(choices=STATUS, default=0)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, default=uuid.uuid1)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    slug = models.SlugField(max_length=50, unique=True, default=uuid.uuid1)
    author = models.CharField(max_length=200)
    text = models.TextField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)
    # number_of_comments = models.CharField(max_length=100)

    def approve(self):
        self.approved_comments = True
        self.save()

    def __str__(self):
        return self.text





