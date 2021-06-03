'''
 将queryset与model实例等进行序列化，转化成json格式，返回给用户(api接口)。
'''
from rest_framework import serializers

from movie.models import Movie


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ['image_link', 'name']
