from hashlib import new
from lib2to3.pytree import convert
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import URL
from .serializers import URLSerializer

import random

# Create your views here.
@api_view(['POST'])
def shortener(request):
    try:    # check if url is in database already
        url = URL.objects.get(link=request.data['link'])
        serializer = URLSerializer(url)
        return Response(serializer.data)        

    except:
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            temp_url = convert()
            new_link = settings.SITE_URL + '/' +str(temp_url)
            serializer.save(new_link=new_link)
            return Response(serializer.data)


def convert():
    encoding = ['a','b','c','d','e','f','g','h','i','j','k','l',
                'm','n','o','p','q','r','s','t','u','v','w','x',
                'y','z',
                'A','B','C','D','E','F','G','H','I','J','K','L',
                'M','N','O','P','Q','R','S','T','U','V','W','X',
                'Y','Z',
                '0','1','2','3','4','5','6','7','8','9']
    while True:
        new_url = ''.join(random.sample(encoding, 8))
        try:
            url = URL.objects.get(new_link=new_url)
        except:
            return new_url


def original(request, short_url):
    new_link = settings.SITE_URL + '/' + str(short_url)
    url = URL.objects.get(new_link=new_link)
    return HttpResponseRedirect(url.link)