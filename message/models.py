from django.db import models
from accounts.models import Profile
from team.models import Team


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender_set')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver_set')
    title = models.CharField(max_length=50, blank=False, null=False)
    content = models.TextField(max_length=5000, blank=False, null=False)
    send_time = models.DateTimeField(auto_now_add=True)
    receiver_visibility = models.BooleanField(default=True)
    sender_visibility = models.BooleanField(default=True)
    read_time = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    is_invite = models.BooleanField(default=True)  # 초대 메세지인지 아닌지
    invite_url = models.URLField(max_length=200, null=True, blank=True)  # 수락 url

    def __str__(self):
        return self.title

class Invite(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_set',)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='invite_sender_set')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='invite_receiver_set')
    is_apply = models.BooleanField(default=False)