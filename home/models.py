from datetime import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Post(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('home:post_detail', args=[self.id, self.slug])

    def get_update_url(self):
        return reverse('home:post_edit', args=[self.id, self.slug])

    def get_delete_url(self):
        return reverse('home:post_delete', args=[self.id, self.slug])

    def like_count(self):
        return self.likes.count()




class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='ccomments', null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}: {self.content[:30]}'


class like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user}: {self.post}'




