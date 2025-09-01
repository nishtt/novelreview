from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home, name="home"),
    path('details/<int:id>/', views.detail, name="detail"),
    path('addnovels/', views.add_novels, name="add_novels"),
    path('editnovels/<int:id>/', views.edit_novels, name="edit_novels"),
    path('deletenovels/<int:id>/', views.delete_novels, name="delete_novels" ),
    path('addreview/<int:id>/', views.add_review, name="add_review" ),
    path('editreview/<int:novel_id>/<int:review_id>/', views.edit_review,  name="edit_review"),
    path('deletereview/<int:novel_id>/<int:review_id>/', views.delete_review,  name="delete_review"),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genres/add/', views.add_genre, name='add_genre'),
    path('genres/edit/<int:id>/', views.edit_genre, name='edit_genre'),
    path('genres/delete/<int:id>/', views.delete_genre, name='delete_genre'),
    path('favorite/<int:novel_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorite/remove/<int:novel_id>/', views.remove_favorite, name='remove_favorite'),
    path('favorites/', views.favorite_list, name='favorite_list'),
]
