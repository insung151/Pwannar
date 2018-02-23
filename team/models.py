from django.db import models
from accounts.models import Profile


class Team(models.Model):
    team_name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(auto_now=True)
    is_activate = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % (self.team_name)


class Member(models.Model):
    member = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )
    position = models.CharField(max_length=20, blank=True, null=True)
    leader = models.BooleanField(default=False)

    def __str__(self):
        return "%s 팀의 %s" % (self.team.team_name, self.member.user)


class Project(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )
    project_name = models.CharField(max_length=20)
    project_description = models.TextField(blank=True, null=True)
    project_end = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s 팀의 %s" % (self.team.team_name, self.project_name)