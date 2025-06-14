from django.urls import path
from calculating_data import views

app_name = 'calculate'
urlpatterns = [
  path('calculating/', views.basic_data, name='calculate_info'),
  path('columns/', views.get_numeric_columns, name='get_num_cols'),
  path('data/', views.calculate_data, name='calculate_data')
]