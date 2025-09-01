from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    query = request.GET.get("title")
    genre_filter = request.GET.get("genre")
    
    novels = Novel.objects.annotate(
        average_rating=Avg('review__rating'),
        review_count=Count('review')
    )
    if genre_filter:
        novels = novels.filter(genres__id=genre_filter)
    
    if query:
        novels = novels.filter(name__icontains=query)
    
    genres = Genre.objects.all().order_by('name')
    
    context = {
        "novels": novels,
        "genres": genres,
        "search_query": query,
        "selected_genre": genre_filter,
    }
    return render(request, 'main/index.html', context)

#detail page
def detail(request, id):
    novel = Novel.objects.prefetch_related('genres').get(id=id)
    reviews = Review.objects.filter(novel=id)
    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    if average == None:
        average=0
    average = round(average, 2)
    review_count=reviews.count()

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, novel=novel).exists()
    context = {
        "novel": novel,
        "reviews": reviews,
        "average": average,
        "review_count": review_count,
        "is_favorite": is_favorite
    }
    return render (request, 'main/details.html', context)

#add novel to db
def add_novels(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form = NovelForm(request.POST or None)

                if form.is_valid():
                    data = form.save()
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
                    data = form.save()
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

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from .models import Novel, Review
from .forms import ReviewForm

@login_required
def genre_list(request):
    genres = Genre.objects.all().order_by('name')
    return render(request, 'main/genre_list.html', {'genres': genres})

@login_required
def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Genre added successfully!')
            return redirect('main:genre_list')
    else:
        form = GenreForm()
    
    return render(request, 'main/add_genre.html', {'form': form})

@login_required
def edit_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            messages.success(request, 'Genre updated successfully!')
            return redirect('main:genre_list')
    else:
        form = GenreForm(instance=genre)
    
    return render(request, 'main/edit_genre.html', {'form': form, 'genre': genre})

@login_required
def delete_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    
    if request.method == 'POST':
        genre.delete()
        messages.success(request, 'Genre deleted successfullly!')
        return redirect('main:genre_list')
    
    return render(request, 'main/delete_genre.html', {'genre': genre})


def add_review(request, id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    
    novel = get_object_or_404(Novel, id=id)
    error_message = None
    
    existing_review = Review.objects.filter(user=request.user, novel=novel).first()
    
    if request.method == "POST":
        if existing_review:
            error_message = "You have already reviewed this novel. You can edit your existing review."
        else:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment', '').strip()
            
            if not rating or not comment:
                error_message = "Please fill out both rating and review fields."
            else:
                review = Review.objects.create(
                    user=request.user,
                    novel=novel,
                    comment=comment,
                    rating=int(rating)
                )
                return redirect("main:detail", id)
    
    reviews = Review.objects.filter(novel=novel)
    average = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'novel': novel,
        'reviews': reviews,
        'average': average,
        'error_message': error_message,
        'existing_review': existing_review 
    }
    
    return render(request, "main/details.html", context)
        

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


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    user = request.user
    user_reviews = Review.objects.filter(user=user).select_related('novel')
    
    total_reviews = user_reviews.count()
    average_rating = user_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'user': user,
        'reviews': user_reviews,
        'total_reviews': total_reviews,
        'average_rating': round(average_rating, 1),
    }
    return render(request, 'main/profile.html', context)

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('main:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'main/edit_profile.html', {'form': form})

def user_profile(request, username):
   
    profile_user = get_object_or_404(User, username=username)
    
    user_reviews = Review.objects.filter(user=profile_user).select_related('novel')
    
    total_reviews = user_reviews.count()
    average_rating = user_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    recent_reviews = user_reviews.order_by('-created_at')[:5]
    
    context = {
        'profile_user': profile_user,
        'reviews': recent_reviews,
        'total_reviews': total_reviews,
        'average_rating': round(average_rating, 1),
        'is_own_profile': request.user == profile_user,
    }
    
    return render(request, 'main/user_profile.html', context)


@login_required
def toggle_favorite(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        novel=novel
    )
    
    if not created:
        favorite.delete()
        message = "Removed from favorites"
    else:
        message = "Added to favorites"
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': message, 'is_favorite': created})
    
    return redirect('main:detail', id=novel_id)

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('novel')
    return render(request, 'main/favorites.html', {'favorites': favorites})