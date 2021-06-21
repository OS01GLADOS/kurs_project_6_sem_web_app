from django.contrib import admin
from .models import Article, Message
from django import forms

class ArticleForm(forms.ModelForm):
    Text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Article
        exclude = ['Liked','Disliked', 'Created','Author', 'Updated']

class ArtilceAdmin(admin.ModelAdmin):
    list_display = ("id", "Title", "Updated")
    form = ArticleForm
    def save_model(self, request, obj, form, change):
        obj.Author = request.user
        super().save_model(request, obj, form, change)

class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "header", "Is_replyed")

admin.site.register(Article, ArtilceAdmin)
admin.site.register(Message, MessageAdmin)

