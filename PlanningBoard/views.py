from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
    )
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from .models import Planning, Tag_Subregion, Tag_Project, Tag_Language, Tag_Region
from .forms import PlanningCreateForm

# Create your views here.

# 목록
def list(request):
    if request.method == "POST":
        selected_all = request.POST.get('city_all')
        selected_city_pk = [] + request.POST.getlist('city')
        if selected_all:
            url = reverse('planningboard:list') + '?selected_all=' + str(selected_all)
        else:
            url = reverse('planningboard:list') + '?selected_city_pk=' + str(selected_city_pk)

        return redirect(url)

    if request.GET.get('selected_all'):
        selected_all = request.GET.get('selected_all')
        detail_list = Planning.objects.filter(subregion__region__pk=selected_all)
        print(detail_list)
        selected_province_pk =  selected_all
        selected_city_pk = []
    else:
        selected_city_pk = eval(request.GET.get('selected_city_pk') or '[]')
        if len(selected_city_pk) == 0:
            detail_list = Planning.objects.all()
            selected_province_pk = 0
        else:
            node = Q(subregion__pk=selected_city_pk[0])
            for pk in selected_city_pk:
                node |= Q(subregion__pk=pk)
            detail_list = Planning.objects.filter(node).distinct()
            selected_province_pk = Tag_Subregion.objects.get(pk=selected_city_pk[0]).region.pk
        selected_all = None

    ctx = {
        'detail_list': detail_list,
        'province_list': Tag_Region.objects.all(),
        'region_list': Tag_Subregion.objects.all(),
        'project_list': Tag_Project.objects.all(),
        'language_list': Tag_Language.objects.all(),
        'selected_province_pk': selected_province_pk,
        'selected_city_pk': selected_city_pk,
        'selected_all': selected_all
    }
    return render (request, 'planning_list.html', ctx)

def alphabet(request):
    detail_list = Planning.objects.order_by('title')
    region_list = Tag_Subregion.objects.all()
    ctx = {
        'detail_list': detail_list,
        'region_list': region_list,
    }
    return render (request, 'list.html', ctx)

def recent(request):
    detail_list = Planning.objects.order_by('-created_at')
    region_list = Tag_Subregion.objects.all()
    ctx = {
        'detail_list': detail_list,
        'region_list': region_list,
    }
    return render (request, 'list.html', ctx)

# 게시글 화면
def detail(request, pk):
    detail = get_object_or_404(Planning, pk=pk)
    ctx = {
        'detail': detail,
        'did_like_article': detail.profile_set.filter(pk=request.user.pk).exists(),
    }
    return render (request, 'detail.html', ctx)

@login_required
def create(request):
    form = PlanningCreateForm(request.user.profile, request.POST or None)
    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        print(request.POST)
        article.save()
        print(article.language.all())
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