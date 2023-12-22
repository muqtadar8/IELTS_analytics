from django.urls import path
from .views import writing_graph, listening_graph, reading_graph    
urlpatterns = [
    path('writing_graph/', writing_graph, name='writing_graph'),
    path('listening_graph/', listening_graph, name='listening_graph'),
    path('reading_graph/', reading_graph, name='reading_graph'),
]