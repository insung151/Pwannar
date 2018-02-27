from django.db import models

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
import datetime


class Info_Article(models.Model):
    title = models.CharField(
        max_length=30,
        verbose_name='제목'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='글쓴이')

    explanation = models.TextField(verbose_name='설명')
    like_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='info_board_article_liked_set',
    )
    recruiting_number = models.IntegerField(
        verbose_name='모집 인원',
    )
    recruiting_period = models.DateField(
        verbose_name='모집 마감일',
        help_text='YYYY-MM-DD 형식으로 입력하세요.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성날짜'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='최종수정날짜'
    )
    image = models.ImageField(upload_to='blog/%Y/%m/%d/', null=True, blank=True, verbose_name='관련정보 포스터', height_field=100, width_field=50)

    url = models.URLField(max_length=200, null=True, blank=True, default='/')

    def image_url(self):
        if self.image:
            image_url = self.image.url
        else:
            image_url = '/static/img/default_img.png'
        return image_url

    def is_today(self):
        return datetime.date.today() == (self.updated_at + datetime.timedelta(hours=9)).date()

    def remain_days(self):
        return (self.recruiting_period-datetime.date.today()).days

    def __str__(self):
        return '{0}.{1}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse('InformationBoard:inform_detail', kwargs={'pk': self.pk})