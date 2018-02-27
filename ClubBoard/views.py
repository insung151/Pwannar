from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Create_Post
from .forms import Create_PostForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@login_required
def blog_detail(request, pk):
    blog_detail = Create_Post.objects.get(pk=pk)
    Create_Post.objects.filter(id=pk).update(view_count=blog_detail.view_count + 1)
    ctx = {
        'detail': blog_detail,
    }

    return render(request, 'blog_detail.html', ctx)


def blog_list(request):
    blog_list = Create_Post.objects.all().order_by('-created_at')

    PAGE_ROW_COUNT = 9
    PAGE_DISPLAY_COUNT = 5

    paginator = Paginator(blog_list, PAGE_ROW_COUNT)
    pageNum = request.GET.get('pageNum')
    totalPageCount = paginator.num_pages
    try:
        blog_list = paginator.page(pageNum)
    except PageNotAnInteger:
        blog_list = paginator.page(1)
        pageNum = 1
    except EmptyPage:
        blog_list = paginator.page(paginator.num_pages)
        pageNum = paginator.num_pages

    pageNum = int(pageNum)

    startPageNum = int(1+((pageNum-1)/PAGE_DISPLAY_COUNT)*PAGE_DISPLAY_COUNT)
    endPageNum = int(startPageNum+PAGE_DISPLAY_COUNT-1)
    if totalPageCount < endPageNum:
        endPageNum = totalPageCount

    bottomPages = range(startPageNum, endPageNum+1)
    ctx = {
        'blog_list': blog_list,
        'pageNum': pageNum,
        'bottomPages': bottomPages,
        'totalPageCount': totalPageCount,
        'startPageNum': startPageNum,
        'endPageNum': endPageNum
    }
    return render(request, 'blog_list.html', ctx)


@login_required
def blog_create(request):
    form = Create_PostForm(request.POST or request.FILES or None)

    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        print(post.pk)
        return redirect(reverse('ClubBoard:blog_detail', kwargs={'pk': post.pk}))

    ctx = {
        'form': form,
    }

    return render(request, 'blog_create.html', ctx)


def blog_delete(request, pk):
    if request.method == "POST":
        detail = get_object_or_404(Create_Post, pk=pk)
        detail.delete()
        return redirect(reverse('ClubBoard:blog_list'))
    else:
        return HttpResponse(status=400)


def blog_edit(request, pk):
    blog_detail = get_object_or_404(Create_Post, pk=pk)
    form = Create_PostForm(request.POST or None, instance=blog_detail)

    if request.method == "POST" and form.is_valid():
        new_form = form.save(commit=False)
        new_form.save()
        return redirect(reverse('ClubBoard:blog_detail', kwargs={'pk': pk}))

    ctx = {
        'form': form,
    }

    return render(request, 'blog_create.html', ctx)


@login_required()
def like(request, pk):
    if request.method == "POST":
        detail = get_object_or_404(Create_Post, pk=pk)

        if request.user.profile.like_club.filter(pk=pk).exists():
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
