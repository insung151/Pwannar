from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Info_Article
from .forms import ArticleForm


def MainPage(request):
    return render(request, 'mainpage.html')


@login_required
def inform_detail(request, pk):
    create_article = get_object_or_404(Info_Article, pk=pk)

    ctx = {
        'detail': create_article,
        'pk': pk,
        'like_article': create_article.like_set.filter(pk=request.user.pk),
    }

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
            article = form.save(commit=False)
            article.author = request.user
            article.save()
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


@login_required
def article_like(request, pk):
    if request.method == "POST":
        article = get_object_or_404(Info_Article, pk=pk)
        if request.user.liked_article_set.filter(pk=pk).exists():
            article.liker_set.remove(request.user)
        else:
            article.liker_set.add(request.user)
        return redirect(article.get_absolute_url())
    else:
        return HttpResponse(status=400)


def inform_edit(request, pk):
    article_detail = get_object_or_404(Info_Article, pk=pk)
    form = ArticleForm(request.POST or None, instance=article_detail)

    if request.method == "POST" and form.is_valid():
        new_form = form.save(commit=False)
        new_form.save()
        return redirect(reverse('InformationBoard:inform_detail', kwargs={'pk': pk}))

    ctx = {
        'form': form,
    }

    return render(request, 'inform_create.html', ctx)

