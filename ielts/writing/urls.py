from django.urls import path 
from . import views

urlpatterns = [
    path('writing/',views.main,  name = 'main')
]
