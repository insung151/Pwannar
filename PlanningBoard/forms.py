from django import forms

from .models import Planning, Tag_Region, Tag_Subregion
from team.models import Team


'''class PlanningCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            profile = kwargs.pop('profile')
        except KeyError:
            print(self.__class__.__name__ + ' requires profile kwarg.')
        super(PlanningCreateForm, self).__init__(*args, **kwargs)

        self.fields['region'].choices = list(Tag_Region.objects.values_list('id', 'name'))
        self.fields['subregion'].choices = list()

        if 'team' in self.fields:
            self.fields['team'].queryset = Team.objects.filter(member__member=profile, member__leader=True)

    class Meta:
        model = Planning
        exclude = ['author', 'created_at', ]
        widgets = {
            'recruiting_period': forms.DateInput(attrs={'class': 'date_picker'})
        }'''

class PlanningCreateForm(forms.ModelForm):
    def __init__(self, profile, *args, **kwargs):
        super(PlanningCreateForm, self).__init__(*args, **kwargs)

        self.fields['region'].choices = list(Tag_Region.objects.values_list('id', 'name'))
        self.fields['subregion'].choices = list()

        self.fields['team'] = forms.ModelChoiceField(
            queryset=Team.objects.filter(member__member=profile, member__leader=True)
        )

    class Meta:
        model = Planning
        exclude = ['author', 'created_at']
        widgets = {
            'recruiting_period': forms.DateInput(attrs={'class': 'date_picker'}),
            'recruiting_number': forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '100'})
        }

    #def clean_recruiting_period():
