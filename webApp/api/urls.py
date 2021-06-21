from django.urls import path
from webApp.api.soap import NewFeedbackService
from webApp.api.views import api_all_article_view
from django.conf.urls import url
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView

app_name = 'webApp'

urlpatterns = [
    path('all-articles',api_all_article_view,name="detail"),
    url(r'^add-feedback-soap', DjangoView.as_view(
        services=[NewFeedbackService], tns='spyne.django',
        in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())),
]