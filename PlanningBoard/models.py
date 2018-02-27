import datetime

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from team.models import Team

class Tag_Region(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True,)

    def __str__(self):
        return self.name

    def get_sebregion(self):
        return list(Tag_Subregion.objects.filter(region__pk=self.pk).values_list('pk', 'name'))

class Tag_Subregion(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True,)
    region = models.ForeignKey(
        Tag_Region,
        on_delete=models.CASCADE,
        null=True,
        related_name='subregions'
        )


    def __str__(self):
        return self.name

class Tag_Project(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True,)

    def __str__(self):
        return self.name

class Tag_Subproject(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True,)

    project = models.ForeignKey(
        Tag_Project,
        on_delete=models.CASCADE,
        related_name='subprojects',
    )

    def __str__(self):
        return self.name

class Tag_Language(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True,)

    def __str__(self):
        return self.name

class Tag_Sublanguage(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True,)

    language = models.ForeignKey(
        Tag_Language,
        on_delete=models.CASCADE,
        related_name='sublanguages'
    )

    def __str__(self):
        return self.name

class Planning(models.Model):
    title = models.CharField(max_length=20, verbose_name='제목', null=True)
    author = models.ForeignKey(User, verbose_name='글쓴이', on_delete=models.CASCADE, related_name='planning_set')
    recruiting_period = models.DateField(blank=True, null=True)
    recruiting_number = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='planning/%Y/%m/%d/', blank=True, null=True,)
    description = models.TextField(blank=True, null=True, verbose_name='설명')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    region = models.ForeignKey(Tag_Region, on_delete=models.CASCADE)
    subregion = models.ManyToManyField(Tag_Subregion)
    language = models.ManyToManyField(Tag_Language)
    project = models.ManyToManyField(Tag_Project)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)


    def image_url(self):
        if self.image:
            image_url = self.image.url
        else:
            image_url = '/static/img/default_img.png'
        return image_url

    # for django template
    def is_today(self):
        return datetime.date.today() == (self.updated_at + datetime.timedelta(hours=9)).date()

    def remain_days(self):
        return (self.recruiting_period-datetime.date.today()).days


class Comment(models.Model):
    detail = models.ForeignKey(
        Planning,
        on_delete=models.CASCADE,
        related_name='comments'
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
        )

    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=100, verbose_name='댓글')

    def __str__(self):
        return self.content