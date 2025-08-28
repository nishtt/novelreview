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
]
