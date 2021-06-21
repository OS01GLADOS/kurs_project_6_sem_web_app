from django.db import connection
from django.shortcuts import render
from .models import Article, Message
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from webApp.forms.Feedback_form_class import FeedbackForm
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.core.mail import send_mail
from kurs_project_server.settings import EMAIL_HOST_USER


def index(request):
    popular_articles = Article.objects.filter(Hidden=False).order_by('-Liked')[:3]
    all_articles = Article.objects.filter(Hidden=False).order_by('-Created')
    context = {
        'pageTitle':'Главная',
        'Article':all_articles,
        'Popular_3_article':popular_articles,
    }
    return render(request, 'webApp/index.html', context)

def feedback_index(request, message_index):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                message_to_update = Message.objects.get(pk=message_index)
                send_mail(
                    form.cleaned_data.get('message_theme'),
                    form.cleaned_data.get('message_text'),
                    EMAIL_HOST_USER,
                    [form.cleaned_data.get('sender_email')],
                    False
                )
                message_to_update.Replyed_by = request.user
                message_to_update.Email = form.cleaned_data.get('sender_email')
                message_to_update.Reply_header = form.cleaned_data.get('message_theme')
                message_to_update.Reply_text = form.cleaned_data.get('message_text')
                message_to_update.save()
                c = connection.cursor()
                try:
                    c.execute("call setmessageasreplyed("+str(message_index)+")")
                finally:
                    c.close()
            return HttpResponseRedirect('/feedback')
        else:
            try:
                message = Message.objects.get(pk=message_index)
            except Message.DoesNotExist:
                raise Http404('сообщение не существует')
            context = {
                'pageTitle':"RE:"+message.header,
                'message':message
            }
            return render(request, 'webApp/feedback_templates/feedback_admin_send.html', context)
    else: raise PermissionDenied()

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            c = connection.cursor()
            try:
                c.execute("call insertmessage('"+form.cleaned_data.get('sender_email')+"','"
                          +form.cleaned_data.get('message_theme')+"','"
                          +form.cleaned_data.get('message_text')+"')")
            finally:
                c.close()
            return HttpResponseRedirect('/')
    else:
        context = {
                'pageTitle':'Обратная связь',
        }
        if request.user.is_authenticated:
            unreplyed_messages = Message.objects.filter(Is_replyed=False)
            template = 'webApp/feedback_templates/feedback_admin.html'
            context['unreplyed_messages'] = unreplyed_messages
        else:
            template = 'webApp/feedback_templates/feedback.html'
        return render(request, template_name=template, context=context)

def article_get_reaction(requset,article_id):
    res = Article.objects.get(id=article_id)
    response_data = {'likes': res.Liked, 'dislikes': res.Disliked}
    return JsonResponse(response_data)

def article(request, article_index):
    try:
        article = Article.objects.get(pk=article_index)
        context = {
            'pageTitle': article.Title,
            'current_article':article,
            'author':article.Author,
            'text': article.Text.replace('\r', '<p>')
        }
        return render(request, 'webApp/article_page.html',context)
    except Article.DoesNotExist:
        raise Http404("Страница не существует")

def article_set_reaction(request, article_id, new_reaction, old_reaction):
    try:
        article_to_react = Article.objects.get(pk=article_id)
    except:
        return Http404('Статья не найдена')
    if new_reaction == 'none':
        if old_reaction == 'like':
            article_to_react.Liked = article_to_react.Liked - 1
        elif old_reaction == 'dislike':
            article_to_react.Disliked = article_to_react.Disliked -1
    elif new_reaction =='like':
        if old_reaction == 'dislike':
            article_to_react.Disliked = article_to_react.Disliked -1
            article_to_react.Liked = article_to_react.Liked +1
        elif old_reaction == 'none':
            article_to_react.Liked = article_to_react.Liked +1
    elif new_reaction == 'dislike':
        if old_reaction == 'like':
            article_to_react.Liked = article_to_react.Liked -1
            article_to_react.Disliked = article_to_react.Disliked +1
        elif old_reaction == 'none':
            article_to_react.Disliked = article_to_react.Disliked +1
    article_to_react.save()
    return HttpResponse(new_reaction+" was setted to article "+str(article_id))