from django.db import models

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User


class Info_Article(models.Model):
    title = models.CharField(
        max_length=30,
        verbose_name='제목'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    explanation = models.TextField(verbose_name='설명')
    like_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='info_board_article_liked_set',
    )
    personnel = models.CharField(
        max_length=30,
        verbose_name='모집 인원'
    )
    due = models.DateTimeField(
        verbose_name='모집 마감일 #YYYY-MM-DD 형식으로 입력하세요.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성날짜'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='최종수정날짜'
    )

    def __str__(self):
        return '{0}.{1}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse('InformationBoard:inform_detail', kwargs={'pk': self.pk})


class Info_Comment(models.Model):
    article = models.ForeignKey(
        Info_Article,
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)