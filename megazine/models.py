from django.db import models
from megazine.utils import random_name_upload_to, thumbnail
from django.db.models.signals import pre_save
from django.core.files import File
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to=random_name_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)
    lnglat = models.CharField(max_length=50, blank=True, null=True, help_text='경도 위도 순으로 입력해주세요 ex)127, 35')

    def __str__(self):
        return self.title

    @property
    def lng(self):
        if self.lnglat:
            return self.lnglat.split(',')[0]

    @property
    def lat(self):
        if self.lnglat:
            return self.lnglat.split(',')[1]


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + self.content

    class Meta:
        ordering = ('-pk', )

def pre_on_post_save(sender, **kargs):
    post = kargs['instance']
    if post.image:
        max_width = 300
        if post.image.width > max_width or post.image.height > max_width:
            processed_file = thumbnail(post.image.file, max_width, max_width)
            post.image.save(post.image.name, File(processed_file))

pre_save.connect(pre_on_post_save, sender=Post)

