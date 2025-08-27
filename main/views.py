from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.
def home(request):
    allNovels = Novel.objects.all()
    
    context = {
        "novels": allNovels,
    }
    return render(request, 'main/index.html', context)

#detail page
def detail(request, id):
    novel = Novel.objects.get(id=id)

    context = {
        "novel": novel
    }
    return render (request, 'main/details.html', context)

#add novel to db
def add_novels(request):
    if request.method == "POST":
        form = NovelForm(request.POST or None)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("main:home")
    else:
        form = NovelForm()
    return render(request, 'main/addnovels.html', {"form": form, "controller": "Add novel"})

def edit_novels(request, id):
    novel = Novel.objects.get(id=id)

    if request.method == "POST":
        form = NovelForm(request.POST or None, instance=novel)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("main:detail", id)
    else:
        form = NovelForm(instance=novel)
    return render(request, 'main/addnovels.html', {"form": form, "controller": "Edit novel"})

def delete_novels(request, id):
    novel = Novel.objects.get(id=id)
    novel.delete()
    return redirect("main:home")
