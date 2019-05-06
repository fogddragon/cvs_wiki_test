import difflib
import json

from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=100, null=False)
    text = models.TextField(max_length=5000, null=False)
    creation_datetime = models.DateTimeField(auto_now=True)


class ArticleChange(models.Model):
    title_diff = models.CharField(max_length=100, null=False)
    text_diff = models.TextField(max_length=5000, null=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    previous_change = models.ForeignKey('ArticleChange', on_delete=models.CASCADE, null=True)
    creation_datetime = models.DateTimeField(auto_now=True)
    is_banned = models.BooleanField(default=False)
    is_current = models.BooleanField(default=True)

    def restore(self):
        return '\n'.join(difflib.restore(json.loads(self.text_diff), 1))
