from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Info_Article, Info_Comment
from .forms import ArticleForm, CommentForm


def MainPage(request):
    return render(request, 'mainpage.html')


@login_required
def inform_detail(request, pk):
    create_article = get_object_or_404(Info_Article, pk=pk)
    comment_form = CommentForm(request.POST or None)

    ctx = {
        'detail': create_article,
        'comment_form': comment_form,
        'pk': pk,
        'did_like_article': create_article.profile_set.filter(pk=request.user.pk).exists(),
    }

    if request.method == "POST" and comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article = create_article
        new_comment.author = request.user
        new_comment.save()
        return redirect(create_article.get_absolute_url())

    return render(request, 'inform_detail.html', ctx)


def inform_list(request):
    inform_list = Info_Article.objects.all()

    ctx = {
        'inform_list': inform_list,
    }
    return render(request, 'inform_list.html', ctx)


@login_required
def inform_create(request):
    form = ArticleForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
            article = form.save()
            return redirect(article.get_absolute_url())

    ctx = {
        'form': form,
    }

    return render(request, 'inform_create.html', ctx)


def inform_update(request, pk):
    article = get_object_or_404(Info_Article, pk=pk)
    form = ArticleForm(request.POST or None, instance=article)

    if request.method == "POST" and form.is_valid():
        article = form.save()
        return redirect(article.get_absolute_url())

    ctx = {
        'form': form,
    }

    return render(request, 'inform_create.html', ctx)


@login_required
def inform_delete(request, pk):
    if request.method == "POST":
        article = get_object_or_404(Info_Article, pk=pk)
        article.delete()
        return redirect(reverse('InformationBoard:inform_list'))
    else:
        return HttpResponse(status=400)

@login_required()
def like(request, pk):
    if request.method == "POST":
        detail = get_object_or_404(Info_Article, pk=pk)

        if request.user.profile.like_info.filter(pk=pk).exists():
            detail.profile_set.remove(request.user.profile)
        else:
            detail.profile_set.add(request.user.profile)
        ctx = {
            'did_like_article': detail.profile_set.filter(pk=request.user.pk).exists(),
            'detail': detail,
        }
        return render(request, 'like_button.html', ctx)
    else:
        return HttpResponse(status=400)