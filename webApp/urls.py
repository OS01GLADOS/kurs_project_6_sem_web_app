from django.urls import path

from  . import  views

app_name = 'webApp'

urlpatterns = [
    path('',views.index, name="index"),
    path('feedback/', views.feedback, name="feedback"),
    path('feedback/<int:message_index>',views.feedback_index, name='feedback-index'),
    path('article/<int:article_index>', views.article, name="article-index"),
    path('article/<int:article_id>/reaction-<str:new_reaction>,prev-<str:old_reaction>',views.article_set_reaction, name='article-reaction-control'),
    path('article/<int:article_id>/get-reaction',views.article_get_reaction, name = 'article-get-reaction')
]