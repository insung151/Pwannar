from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse

from .models import Member, Team, Project
from .forms import TeamForm, MemberForm, ProjectForm


def create_team(request):
    team_form = TeamForm(request.POST or None)
    user = request.user.profile
    if request.method == "POST" and team_form.is_valid():
        new_team = team_form.save()
        team_member = Member(
            member=user,
            team=new_team,
            position='팀장',
            leader=True,
        )
        team_member.save()
        return redirect(reverse(
            'accounts:myinfo',
            kwargs={'username': request.user.username}
        ))
    ctx = {
        'form': team_form,
    }
    return render(request, 'createteam.html', ctx)


def manage_team(request, team_name):
    team = get_object_or_404(Team, team_name=team_name)
    team_members = Member.objects.filter(team=team)
    ctx = {
        'team': team,
        'team_members': team_members,
    }
    return render(request, 'manage_team.html', ctx)


def delete_team(request, team_name):
    if request.method == "POST":
        team = get_object_or_404(Team, team_name=team_name)
        team.delete()
        return redirect(reverse(
            'accounts:myinfo',
            kwargs={'username': request.user.username}
        ))
    else:
        return HttpResponse(status=400)


def start_project(request, team_name):
    project_form = ProjectForm(request.POST or None)
    team = Team.objects.filter(member__member=request.user.profile)
    if request.method == "POST" and project_form.is_valid():
        new_project = project_form.save(commit=False)
        new_project.team = Team.objects.get(team_name=team_name)
        new_project.save()
        return redirect(reverse(
            'team:manage_team',
            kwargs={'team_name': team_name}
        ))
    ctx = {
        'form': project_form
    }
    return render(request, 'startproject.html', ctx)


# def delete_project(request, pk):
#     team = Project.objects.get(pk=pk).team
#     if request.method == "POST" and request.user.profile == Member.objects.get(team=team, leader=True).member:
#         team_project = get_object_or_404(Project, pk=pk)
#         team_project.delete()
#         return render(request, 'project_list.html')
#     else:
#         HttpResponse(status=400)



def finish_project(request):
    pass


def manage_member(request):
    pass


