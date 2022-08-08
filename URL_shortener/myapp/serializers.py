from nturl2path import url2pathname
from rest_framework import serializers
from .models import URL

# convert data to json format to communicate with frontend
class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = '__all__'
