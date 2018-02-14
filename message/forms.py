# Created by Inseong on 2018-02-05

# Created by Inseong on 2018-02-05
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('sender', 'receiver', 'send_time', 'sender_visibility', 'receiver_visibility', 'read_time', 'is_read')

class InviteForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)