from django.urls import path
from visualization import views

app_name = 'diagrams'

urlpatterns = [
    path('graphs/', views.visualization_type, name='graph')
]