from django.db.models import Q
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
    )
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from .models import Planning, Tag_Subregion, Tag_Project, Tag_Language, Tag_Region
from .forms import PlanningCreateForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
        selected_province_pk = selected_all
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
    return render(request, 'planning_list.html', ctx)


def alphabet(request):
    detail_list = Planning.objects.order_by('title')
    region_list = Tag_Subregion.objects.all()
    ctx = {
        'detail_list': detail_list,
        'region_list': region_list,
    }
    return render(request, 'list.html', ctx)


def recent(request):
    detail_list = Planning.objects.order_by('-created_at')
    region_list = Tag_Subregion.objects.all()
    ctx = {
        'detail_list': detail_list,
        'region_list': region_list,
    }
    return render(request, 'list.html', ctx)


# 게시글 화면
def detail(request, pk):
    detail = get_object_or_404(Planning, pk=pk)
    ctx = {
        'detail': detail,
    }
    return render(request, 'detail.html', ctx)


'''@login_required
def create(request):
    form = PlanningCreateForm(
        request.POST or None,
        request.FILES or None,
        profile=request.user.profile,
    )
    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        print(request.POST)
        article.save()
        form.save_m2m()
        print(article.language.all())
        return redirect(reverse('planningboard:detail', kwargs={'pk': article.pk,}))

    ctx = {
        'form': form,
        'region': Tag_Region.objects.all(),
        'subregion': Tag_Subregion.objects.all()
    }
    return render(request, 'create.html', ctx)'''

@login_required
def create(request):
    form = PlanningCreateForm(request.user.profile, request.POST or None, request.FILES or None,)
    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.author = request.user

        article.save()
        form.save_m2m()

        return redirect(reverse('planningboard:detail', kwargs={'pk': article.pk}))
    ctx = {
        'form': form,
        'region': Tag_Region.objects.all(),
        'subregion': Tag_Subregion.objects.all()
    }
    return render(request, 'create.html', ctx)

'''@login_required
def update(request, pk):
    detail = get_object_or_404(Planning, pk=pk)
    form = PlanningCreateForm(request.POST or None, instance=detail)
    if request.method == "POST" and form.is_valid():
        #new_form = form.save(commit=False)
        # new_form.author = request.user
        # new_form.tag_set = request.user.tag_set.all()
        planning = form.save()
        return redirect(planning.get_absolute_url())
    ctx = {
        'form': form
    }

    return render(request, 'create.html', ctx)'''


@login_required
def update(request, pk):
    detail = get_object_or_404(Planning, pk=pk)
    form = PlanningCreateForm(request.POST or None, instance=detail,)
    if request.method == "POST" and form.is_valid():
        new_form = form.save(commit=False)
        # new_form.author = request.user
        # new_form.tag_set = request.user.tag_set.all()
        planning = new_form.save()
        return redirect(planning.get_absolute_url())
    ctx = {
        'form': form
    }
    return render(request, 'create.html', ctx)


@login_required
def delete(request, pk):
    if request.method == "POST":
        detail = get_object_or_404(Planning, pk=pk)
        detail.delete()
        return redirect(reverse('planningboard:list'))
    else:
        return HttpResponse(status=400)


def get_subegion(request, pk):
    if request.method == "POST":
        subregion_list = Tag_Region.objects.get(pk=pk).get_sebregion()
        print(subregion_list)
        return render(request, 'subregion.html', {'subregion_list': subregion_list})

'''
def list(request):
    PAGE_ROW_COUNT = 5
    PAGE_DISPLAY_COUNT = 5

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
        selected_province_pk = selected_all
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

    total_list = Planning.objects.all().order_by('-num')
    paginator = Paginator(total_list, PAGE_ROW_COUNT)
    pageNum = request.GET.get('pageNum')
    totalPageCount = paginator.num_pages  #전체 페이지 개수
    try:
        planning_list = paginator.page(pageNum)
    except PageNotAnInteger:
        planning_list = paginator.page(1)
        pageNum = 1
    except EmptyPage:
        planning_list = paginator.page(paginator.num_pages)
        pageNum = paginator.num_pages

    pageNum = int(pageNum)

    startPageNum = int(1+((pageNum-1)/PAGE_DISPLAY_COUNT)*PAGE_DISPLAY_COUNT)
    endPageNum = int(startPageNum+PAGE_DISPLAY_COUNT-1)
    if totalPageCount < endPageNum:
        endPageNum = totalPageCount

    bottomPages = range(startPageNum, endPageNum+1)

    ctx = {
        'detail_list': detail_list,
        'province_list': Tag_Region.objects.all(),
        'region_list': Tag_Subregion.objects.all(),
        'project_list': Tag_Project.objects.all(),
        'language_list': Tag_Language.objects.all(),
        'selected_province_pk': selected_province_pk,
        'selected_city_pk': selected_city_pk,
        'selected_all': selected_all,
        'planning_list': planning_list,
        'pageNum': pageNum,
        'bottomPages': bottomPages,
        'totalPageCount': totalPageCount,
        'startPageNum': startPageNum,
        'endPageNum': endPageNum
    }
    return render(request, 'planning_list.html', ctx)'''
