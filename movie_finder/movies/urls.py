from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('recommend/', views.recommend, name='movies-recomend'),
]
