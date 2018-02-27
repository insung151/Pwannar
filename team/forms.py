from django import forms
from .models import Team, Member, Project


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('team_name',)


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('position',)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name', 'project_description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project_description'].initial = '언어 : \nOS : \n'
