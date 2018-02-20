from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
#from datetime import datetime


class Create_Post(models.Model):
    title = models.CharField(
        max_length=30,
        verbose_name='제목',
        null=True,
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='글쓴이')
    club_name = models.TextField(verbose_name='동아리 이름', default='예시: 피로그래밍')
    recruiting_period = models.DateTimeField(
        null = True, blank = True,
        verbose_name='모집 마감일 #YYYY-MM-DD 형식으로 입력하세요.'
    )
    recruiting_number = models.CharField(
        max_length=30,
        verbose_name='모집 인원',
        null = True, blank = True,
    )
    description = models.TextField(verbose_name='설명')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성 날짜'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='최종 수정 날짜'
    )
    like_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='club_board_article_liked_set',
    )

    image = models.ImageField(upload_to='blog/%Y/%m/%d/', null=True, blank=True, verbose_name='동아리 포스터')

    view_count = models.IntegerField(default=0, null=True)

    def image_url(self):
        if self.image:
            image_url = self.image.url
        else:
            image_url = '/static/img/default_img.png'
        return image_url


    def __str__(self):
        return '{0}.{1}'.format(self.pk, self.title)


