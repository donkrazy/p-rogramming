from django.db import models
from django.core.files import File
from django.db.models.signals import pre_save
from blog.utils import random_name_upload_to, square_image, thumbnail


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to=random_name_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


def pre_on_post_save(sender, **kargs):
    post = kargs['instance']
    if post.image:
        max_width = 300
        if post.image.width > max_width or post.image.height > max_width:
            processed_file = thumbnail(post.image.file, max_width, max_width)
            post.image.save(post.image.name, File(processed_file))

pre_save.connect(pre_on_post_save, sender=Post)

class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
