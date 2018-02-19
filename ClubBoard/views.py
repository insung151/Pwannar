from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse #Http404
from django.contrib.auth.decorators import login_required
from .models import Create_Post
from .forms import Create_PostForm



#@login_required
def blog_detail(request, pk):
    blog_detail = Create_Post.objects.get(pk=pk)
    print(blog_detail)
    ctx = {
        'blog_detail': blog_detail,
    }

    return render(request, 'ClubBoard/blog_detail.html', ctx)


def blog_list(request):
    blog_list =Create_Post.objects.all().order_by('-created_at') #####

    ctx = {
        'blog_list': blog_list,
    }
    return render(request, 'ClubBoard/blog_list.html', ctx)



#@login_required
def blog_create(request):
    form = Create_PostForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.save()
        print(post.pk)
        return redirect(reverse('ClubBoard:blog_detail', kwargs={'pk': post.pk}))

    ctx = {
        'form': form,
    }

    return render(request, 'ClubBoard/blog_create.html', ctx)


def blog_edit(request, pk):
    blog_detail = get_object_or_404(Create_Post, pk=pk)
    form = Create_PostForm(request.POST or None, instance=blog_detail)

    if request.method == "POST" and form.is_valid():
        new_form = form.save(commit=False)
        new_form.save()
        return redirect(reverse('CluaBoard/blog_detail', kwargs={'pk': pk}))

    ctx = {
        'form': form,
    }

    return render(request, 'ClubBoard/blog_create.html', ctx)
