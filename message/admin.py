from django.contrib import admin
from .models import Message, Invite

admin.site.register(Message)
admin.site.register(Invite)