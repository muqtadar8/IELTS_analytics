from django.urls import path
from .views import plot_view

urlpatterns = [
    path('graph/', plot_view, name='plot_view'),
]