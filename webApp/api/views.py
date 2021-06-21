from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from webApp.models import Article
from webApp.api.serializers import ArticleSerializer

@api_view(['GET'])
def  api_all_article_view(requset):
    try:
        request_date_time = parse_datetime(requset.headers['Date'])
        print(request_date_time)
        all_article = Article.objects.filter(Updated__gte=request_date_time).filter(Hidden=False)
    except:
        print("no date was sended")
        all_article = Article.objects.filter(Hidden=False)
    serializer = ArticleSerializer(all_article,many=True)
    response_to_send = Response(serializer.data)
    response_to_send['Date'] = timezone.now()

    return response_to_send