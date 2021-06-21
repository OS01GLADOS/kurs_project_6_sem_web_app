from django import forms
from webApp.models import Message


class FeedbackForm(forms.ModelForm):
    sender_email = forms.CharField(label='sender_email', max_length=100)
    message_theme = forms.CharField(label='message_theme', max_length=100)
    message_text = forms.CharField(label='message_text',max_length=1000)
    class Meta:
        model = Message
        fields = ('sender_email','message_text', 'message_theme')