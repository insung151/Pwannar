from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from accounts.models import Profile
from team.models import Team, Member
from .models import Message, Invite
from .forms import MessageForm, InviteForm


@login_required
def message_list(request):
    messages = request.user.profile.receiver_set.filter(receiver_visibility=True)
    ctx = {
        'messages': messages
    }
    return render(request, 'message_list.html', ctx)

def message_detail(request, pk):
    message = Message.objects.get(pk=pk)
    if not (message.sender == request.user.profile or message.receiver == request.user.profile):
        raise Http404('권한이 없습니다.')
    if request.user.profile == message.receiver and not message.is_read:
        message.is_read = True
        message.save()
    ctx = {
        'message': message,
    }
    return render(request, 'message_detail.html', ctx)

def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == "POST":
        if request.user.profile == message.receiver:
            message.receiver_visibility = False
            message.save()
            if not message.sender_visibility:
                message.delete()
            return redirect('message:messages')
        elif request.user.profile == message.sender:
            message.sender_visibility = False
            message.save()
            if not message.receiver_visibility:
                message.delete()
            return redirect('message:send_messages')
    else:
        raise Http404('잘못된 접근입니다.')

@login_required()
def send_message(request, username):
    message_form = MessageForm(request.POST or None)
    receiver = get_object_or_404(User, username=username).profile
    if request.method == 'POST':
        message = message_form.save(commit=False)
        message.receiver = receiver
        message.sender = request.user.profile
        message.save()
        return redirect('message:send_messages')
    else:
        ctx = {'form': message_form, 'receiver': username}
        return render(request, 'message_send.html', ctx)


@login_required()
def send_message_list(request):
    messages = request.user.profile.sender_set.filter(sender_visibility = True)
    ctx = {
        'messages': messages,
    }
    return render(request, 'send_message_list.html', ctx)

@login_required()
def invite(request, username):
    receiver = User.objects.get(username=username).profile
    invite_form = InviteForm(request.POST or None)
    if request.method == "POST" and request.POST.get('team_list'):
        team_pk = request.POST['team_list'][0]
        team = Team.objects.get(pk=team_pk)
        message = invite_form.save(commit=False)
        message.title = str(team.team_name) + "으로 초대합니다."
        message.receiver = receiver
        invite = Invite.objects.create(team=team, sender=request.user.profile, receiver=receiver)
        message.content = str(get_current_site(request).domain)+str(reverse('message:join', kwargs={'pk': invite.pk}))
        message.sender = request.user.profile
        message.save()
        return HttpResponse('초대메시지가 전송되었습니다.')
    ctx = {
        'form': invite_form,
        'team_list': Team.objects.filter(member__member=request.user.profile, member__leader=True)
    }
    return render(request, 'invite.html', ctx)


def accept(request, pk):
    invite = get_object_or_404(Invite, pk=pk)
    invite_team = invite.team
    already_in = False  #이미 가입되어 있는 팀인지 확인
    for member in request.user.profile.member_set.all():
        if member.team == invite_team:
            already_in = True
            break
    if already_in:
        raise Http404('이미 가입된 팀 입니다.')
    if request.user.profile != invite.receiver:
        raise Http404('잘못된 경로입니다.')
    ctx = {
        'invite': invite,
    }
    return render(request, 'accept.html', ctx)


def join(request, pk):
    invite = get_object_or_404(Invite, pk=pk)
    already_in = False  # 이미 가입되어 있는 팀인지 확인
    for member in request.user.profile.member_set.all():
        if member.team == invite.team:
            already_in = True
            break
    if already_in:
        raise Http404('이미 가입된 팀 입니다.')
    if request.user.profile != invite.receiver:
        raise Http404('잘못된 경로입니다.')
    Member.objects.create(team=invite.team, member=request.user.profile)
    invite.delete()
    return redirect(reverse('accounts:myinfo', kwargs={'username':request.user.username}))