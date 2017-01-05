from django.db import models
from uuid import uuid4


class EmailToken(models.Model):
    email = models.EmailField(max_length=255)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.token = str(uuid4())
        super(EmailToken, self).save(*args, **kwargs)
