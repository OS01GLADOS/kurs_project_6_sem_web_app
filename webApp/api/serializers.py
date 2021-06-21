from webApp.models import Article
from rest_framework import serializers
import base64

class ArticleSerializer(serializers.ModelSerializer):
    Author_Full = serializers.SerializerMethodField(method_name='author_full_name')
    Created_date_time = serializers.SerializerMethodField(method_name='created_date_format')
    Image_64 = serializers.SerializerMethodField(method_name='image_to_base64')

    def image_to_base64(self, instance):
        with open('media/'+str(instance.Photo), "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    def created_date_format(self, instance):
        return str(instance.Updated.day)+"/"+str(instance.Updated.month)+"/"+str(instance.Updated.year)+' '+str(instance.Updated.hour)+":"+str(instance.Updated.minute)
    def author_full_name(self,instance):
        return instance.Author.first_name + " "+instance.Author.last_name

    class Meta:
        model = Article
        fields = ('id','Title','Preambule','Text','Author_Full','Image_64','Created_date_time',)