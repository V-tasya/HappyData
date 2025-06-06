from django.urls import path
from interface import views

urlpatterns = [
  path('', views.main_page),
  path('analysis/', views.analysis_page)
]
