from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
import datetime
from .models import Article, Tag
from .forms import ArticleForm, CommentForm
from ClubBoard.models import Create_Post
from InformationBoard.models import Info_Article
from PlanningBoard.models import Planning
from team.models import Team, Project
from message.models import Message


def MainPage(request):
    now = datetime.datetime.now()
    seven_days = datetime.timedelta(weeks=1)
    for i in range(0, 7):
        target_day = now - datetime.timedelta(days=i)
        if target_day.weekday() == 0 :
            monday = target_day.replace(hour=0, minute=0, second=0, microsecond=0)
    planningboard_count = Planning.objects.filter(created_at__range=(monday, monday+seven_days)).count()
    clubboard_count = Create_Post.objects.filter(created_at__range=(monday, monday+seven_days)).count()
    infoboard_count = Info_Article.objects.filter(created_at__range=(monday, monday+seven_days)).count()


    if request.user.pk != None:
        project_list = Project.objects.filter(team__member__member=request.user.profile)
        message_list = Message.objects.filter(receiver = request.user.profile)
    else:
        project_list = []
        message_list = []
    new_message_list = []
    for message in message_list:
        if message.is_read == False:
            new_message_list.append(message)

    ctx = {
        'monday': monday,
        'planningboard_count': planningboard_count,
        'clubboard_count': clubboard_count,
        'infoboard_count': infoboard_count,
        'project_list': project_list,
        'message_list': new_message_list,
    }
    return render(request, 'mainpage.html', ctx)


@login_required
def board_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm(request.POST or None)
    ctx = {
        'article': article,
        'comment_form': comment_form,
        'pk': pk,
        'did_like_article': article.liker_set.filter(pk=request.user.pk),
    }

    if request.method == "POST" and comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article = article
        new_comment.author = request.user
        new_comment.save()
        return redirect(article.get_absolute_url())

    return render(request, 'board_detail.html', ctx)


def board_list(request, tag_pk=None):
    if tag_pk is not None:
        article_list = Article.objects.filter(tag__pk=tag_pk)
        try:
            tag = Tag.objects.get(pk=tag_pk)
        except Tag.DoesNotExist:
            raise Http404('없는 Tag입니다.')
    else:
        article_list = Article.objects.all()
        tag = None

    ctx = {
        'board_list': article_list,
        'tag_list': Tag.objects.all(),
        'tag_selected': tag,
    }

    return render(request, 'board_list.html', ctx)


@login_required
def board_create(request):
    form = ArticleForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
            article = form.save()

            return redirect(article.get_absolute_url())

    ctx = {
        'form': form,
    }

    return render(request, 'board_create.html', ctx)


def board_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(request.POST or None, instance=article)

    if request.method == "POST" and form.is_valid():
        article = form.save()
        return redirect(article.get_absolute_url())

    ctx = {
        'form': form,
    }

    return render(request, 'board_create.html', ctx)


@login_required
def board_delete(request, pk):
    if request.method == "POST":
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return redirect(reverse('core:board_list'))
    else:
        return HttpResponse(status=400)


@login_required
def article_like(request, pk):
    if request.method == "POST":
        article = get_object_or_404(Article, pk=pk)
        if request.user.liked_article_set.filter(pk=pk).exists():
            article.liker_set.remove(request.user)
        else:
            article.liker_set.add(request.user)
        return redirect(article.get_absolute_url())
    else:
        return HttpResponse(status=400)
