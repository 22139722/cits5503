from django.conf import settings
from django.shortcuts import render
from lib.utils import boto_client
from pprint import pprint


def home(request):
    c = {}
    return render(request, 'lib/base.html', c)