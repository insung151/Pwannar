from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
    )
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse


from .models import (
    Planning,
    Tag_Subregion,
    Tag_Project,
    Tag_Language,
    Tag_Region,
    Comment
    )

from .forms import (
    PlanningCreateForm,
    CommentForm
    )

# Create your views here.

# 목록
def detail_list(request):
    if request.method == "POST":
        selected_region_all = request.POST.get('city_all')
        selected_city_pk = [] + request.POST.getlist('city')
        selected_project_pk = [] + request.POST.getlist('project')
        selected_language_pk = [] +request.POST.getlist('language')

        url = reverse('planningboard:list')
        if selected_region_all:
            url += '?selected_region_all=' + str(selected_region_all)
        else:
            url += '?selected_city_pk=' + str(selected_city_pk)

        if request.POST.get('language_all'):
            url += '&selected_language_pk=' + str(list(map(lambda x:x.get('pk'), Tag_Language.objects.values('pk'))))
        else:
            url += '&selected_language_pk=' + str(selected_language_pk)

        if request.POST.get('project_all'):
            url += '&selected_project_pk=' + str(list(map(lambda x: x.get('pk'),Tag_Project.objects.values('pk'))))
        else:
            url += '&selected_project_pk' + str(selected_project_pk)

        return redirect(url)

    selected_language_pk = eval(request.GET.get('selected_language_pk') or '[]')
    selected_project_pk = eval(request.GET.get('selected_project_pk') or '[]')
    detail_list = Planning.objects.filter()

    if selected_language_pk:
        node = Q(language__pk=selected_language_pk[0])
        for pk in selected_language_pk:
            node |= Q(language__pk=pk)
        detail_list = detail_list.filter(node).distinct()

    if selected_project_pk:
        node = Q(project__pk=selected_project_pk[0])
        for pk in selected_project_pk:
            node |= Q(project__pk=pk)
        detail_list = detail_list.filter(node).distinct()

    if request.GET.get('selected_region_all'):
        selected_region_all = request.GET.get('selected_region_all')
        detail_list = detail_list.filter(region__pk=selected_region_all)
        selected_province_pk =  selected_region_all
        selected_city_pk = []
    else:
        selected_city_pk = eval(request.GET.get('selected_city_pk') or '[]')
        if len(selected_city_pk) == 0:
            selected_province_pk = 0
        else:
            node = Q(subregion__pk=selected_city_pk[0])
            for pk in selected_city_pk:
                node |= Q(subregion__pk=pk)
            detail_list = detail_list.filter(node).distinct()
            selected_province_pk = Tag_Subregion.objects.get(pk=selected_city_pk[0]).region.pk
        selected_region_all = None

    ctx = {
        'detail_list': detail_list.order_by('-created_at'),
        'province_list': Tag_Region.objects.all(),
        'region_list': Tag_Subregion.objects.all(),
        'project_list': Tag_Project.objects.all(),
        'language_list': Tag_Language.objects.all(),
        'selected_province_pk': selected_province_pk,
        'selected_city_pk': selected_city_pk,
        'selected_region_all': selected_region_all,
        'selected_language_pk': selected_language_pk,
        'selected_project_pk': selected_project_pk,
    }
    return render (request, 'planning_list.html', ctx)

def detail_list_html(request):
    selected_language_pk = eval(request.GET.get('selected_language_pk') or '[]')
    selected_project_pk = eval(request.GET.get('selected_project_pk') or '[]')
    detail_list = Planning.objects.filter()
    if selected_language_pk:
        node = Q(language__pk=selected_language_pk[0])
        for pk in selected_language_pk:
            node |= Q(language__pk=pk)
            detail_list = detail_list.filter(node).distinct()

    if selected_project_pk:
        node = Q(project__pk=selected_project_pk[0])
        for pk in selected_project_pk:
            node |= Q(project__pk=pk)
            detail_list = detail_list.filter(node).distinct()

    if request.GET.get('selected_region_all'):
        selected_region_all = request.GET.get('selected_region_all')
        detail_list = detail_list.filter(region__pk=selected_region_all)
        selected_province_pk = selected_region_all
        selected_city_pk = []
    else:
        selected_city_pk = eval(request.GET.get('selected_city_pk') or '[]')
        if len(selected_city_pk) == 0:
            selected_province_pk = 0
        else:
            node = Q(subregion__pk=selected_city_pk[0])
            for pk in selected_city_pk:
                node |= Q(subregion__pk=pk)
            detail_list = detail_list.filter(node).distinct()
            selected_province_pk = Tag_Subregion.objects.get(pk=selected_city_pk[0]).region.pk
        selected_region_all = None

    ctx = {
        'detail_list': detail_list.order_by('-created_at'),
        'province_list': Tag_Region.objects.all(),
        'region_list': Tag_Subregion.objects.all(),
        'project_list': Tag_Project.objects.all(),
        'language_list': Tag_Language.objects.all(),
        'selected_province_pk': selected_province_pk,
        'selected_city_pk': selected_city_pk,
        'selected_region_all': selected_region_all,
        'selected_language_pk': selected_language_pk,
        'selected_project_pk': selected_project_pk,
    }
    return render(request, 'detail_list.html', ctx)

def alphabet(request):
    selected_detail_list = request.POST.getlist('selected_detail_list[]')
    unordered_detail_list = Planning.objects.none()

    for detail_pk in selected_detail_list:
        unordered_detail_list |= Planning.objects.filter(pk=detail_pk)
    detail_list = unordered_detail_list.order_by('title')

    return render(request, 'detail_list.html', {'detail_list': detail_list})

def recent(request):
    selected_detail_list = request.POST.getlist('selected_detail_list[]')
    unordered_detail_list = Planning.objects.none()

    for detail_pk in selected_detail_list:
        unordered_detail_list |= Planning.objects.filter(pk=detail_pk)
    detail_list = unordered_detail_list.order_by('-created_at')

    return render(request, 'detail_list.html', {'detail_list': detail_list})

# 게시글 화면
def detail(request, pk):
    detail = get_object_or_404(Planning, pk=pk)
    comment_list = Comment.objects.filter(detail__pk=detail.pk).order_by('-created_at')
    comment_form = CommentForm(request.POST or None)
    ctx = {
        'detail': detail,
        'did_like_article': detail.profile_set.filter(pk=request.user.pk).exists(),
        'comment_list': comment_list,
        'comment_form': comment_form,
    }
    return render (request, 'detail.html', ctx)

@login_required
def create(request):
    form = PlanningCreateForm(request.user.profile, request.POST or None)
    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.author = request.user

        article.save()
        form.save_m2m()

        return redirect(reverse('planningboard:detail', kwargs={'pk': article.pk}))
    ctx = {
        'form': form,
        'region':Tag_Region.objects.all(),
        'subregion':Tag_Subregion.objects.all()
    }
    return render (request, 'create.html', ctx)

def update(request, pk):
    detail = get_object_or_404(Planning, pk=pk)
    form = PlanningCreateForm(request.POST or None, instance=detail)
    if request.method == "POST" and form.is_valid():
       new_form = form.save(commit=False)
       # new_form.author = request.user
       # new_form.tag_set = request.user.tag_set.all()
       new_form.save()
       form.save_m2m()
       return redirect(reverse('planningboard:detail', kwargs={'pk': pk}))
    ctx = {
        'form': form
    }
    return render(request, 'create.html', ctx)

def get_subegion(request, pk):
    if request.method == "POST":
        subregion_list = Tag_Region.objects.get(pk=pk).get_sebregion()
        return render(request, 'subregion.html',{'subregion_list': subregion_list})

def like(request, pk):
    if request.method == "POST":
        detail = get_object_or_404(Planning, pk=pk)

        if request.user.profile.like_planning.filter(pk=pk).exists():
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

        print(subregion_list)
        return render(request, 'subregion.html',{'subregion_list': subregion_list})

def comment_create(request, detail_pk):

    if request.method == "POST":
        detail = Planning.objects.get(pk=detail_pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.detail = detail
            new_comment.save()
            return render(request, 'comment_list.html', {'comment': new_comment})
    return HttpResponse(status=405)