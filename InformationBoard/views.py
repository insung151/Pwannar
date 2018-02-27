from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Info_Article
from .forms import ArticleForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def MainPage(request):
    return render(request, 'mainpage.html')


@login_required
def inform_detail(request, pk):
    create_article = get_object_or_404(Info_Article, pk=pk)

    ctx = {
        'detail': create_article,
        'pk': pk,
        'did_like_article': create_article.profile_set.filter(pk=request.user.pk).exists(),
    }

    return render(request, 'inform_detail.html', ctx)


def inform_list(request):
    inform_list = Info_Article.objects.all()

    PAGE_ROW_COUNT = 5
    PAGE_DISPLAY_COUNT = 5

    paginator = Paginator(inform_list, PAGE_ROW_COUNT)
    pageNum = request.GET.get('pageNum')
    totalPageCount = paginator.num_pages
    try:
        inform_list = paginator.page(pageNum)
    except PageNotAnInteger:
        inform_list = paginator.page(1)
        pageNum = 1
    except EmptyPage:
        inform_list = paginator.page(paginator.num_pages)
        pageNum = paginator.num_pages

    pageNum = int(pageNum)

    startPageNum = int(1+((pageNum-1)/PAGE_DISPLAY_COUNT)*PAGE_DISPLAY_COUNT)
    endPageNum = int(startPageNum+PAGE_DISPLAY_COUNT-1)
    if totalPageCount < endPageNum:
        endPageNum = totalPageCount

    bottomPages = range(startPageNum, endPageNum+1)
    ctx = {
        'inform_list': inform_list,
        'pageNum': pageNum,
        'bottomPages': bottomPages,
        'totalPageCount': totalPageCount,
        'startPageNum': startPageNum,
        'endPageNum': endPageNum
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
