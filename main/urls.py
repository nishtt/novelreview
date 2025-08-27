from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home, name="home"),
    path('details/<int:id>/', views.detail, name="detail"),
    path('addnovels/', views.add_novels, name="add_novels"),
    path('editnovels/<int:id>/', views.edit_novels, name="edit_novels"),
    path('deletenovels/<int:id>/', views.delete_novels, name="delete_novels" )
]
