from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Avg

# Create your views here.
def home(request):
    query = request.GET.get("title")
    allNovels = None
    if query:
        allNovels = Novel.objects.filter(name__icontains=query)
    else:
        allNovels = Novel.objects.all()
    
    context = {
        "novels": allNovels,
    }
    return render(request, 'main/index.html', context)

#detail page
def detail(request, id):
    novel = Novel.objects.get(id=id)
    reviews = Review.objects.filter(novel=id)
    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    if average == None:
        average=0
    average = round(average, 2)
    context = {
        "novel": novel,
        "reviews": reviews,
        "average": average
    }
    return render (request, 'main/details.html', context)

#add novel to db
def add_novels(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form = NovelForm(request.POST or None)

                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:home")
            else:
                form = NovelForm()
            return render(request, 'main/addnovels.html', {"form": form, "controller": "Add novel"})
        else:
            return redirect("main:home")
    return redirect("accounts:login")

def edit_novels(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
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
        else:
            return redirect("main:home")
    return redirect("accounts:login")

def delete_novels(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            novel = Novel.objects.get(id=id)
            novel.delete()
            return redirect("main:home")
        else:
            return redirect("main:home")
    return redirect("accounts:login")

def add_review(request, id):
    if request.user.is_authenticated:
        novel = Novel.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST.get("comment")
                data.rating = request.POST.get("rating")
                data.user = request.user
                data.novel = novel
                data.save()
                return redirect("main:detail", id)
            else:
                form = ReviewForm()
            return render(request, "main/details.html", {"form":form})
        else:
            return redirect("accounts:login")
        

#edit review
def edit_review(request, novel_id, review_id):
    if request.user.is_authenticated:
        novel = Novel.objects.get(id=novel_id)
        review = Review.objects.get(novel=novel, id=review_id)

        if request.user == review.user:
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = "Out of range. Select rating from 0 to 10"
                        return render(request, "main/editreview.html", {"error":error, "form":form})
                    else:
                        data.save()
                        return redirect("main:detail", novel_id)
                
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html', {"form":form})
        else:
            return redirect("main:detail", novel_id)
    else:
        return redirect("accounts:login")


def delete_review(request, novel_id, review_id):
    if request.user.is_authenticated:
        novel = Novel.objects.get(id=novel_id)
        review = Review.objects.get(novel=novel, id=review_id)

        if request.user == review.user:
          review.delete()
        
        return redirect("main:detail", novel_id)
    else:
        return redirect("accounts:login")