from django.db import models
from django.utils import timezone

from user.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=130, blank=False)
    like = models.ManyToManyField(User, related_name='related_post', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-created_at"]
