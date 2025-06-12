from django.urls import path
from calculating_data import views

app_name = 'calculate'
urlpatterns = [
  path('calculating/', views.basic_info, name='calculate_data')
]