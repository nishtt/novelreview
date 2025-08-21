from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def home(request):
    allNovels = Novel.objects.all()
    print(allNovels)
    return render(request, 'main/index.html')
    