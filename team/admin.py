from django.contrib import admin
from .models import Team, Member, Project


admin.site.register(Team)
admin.site.register(Member)
admin.site.register(Project)