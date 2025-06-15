from django.urls import path
from linear_regression import views

app_name = 'regression'
urlpatterns = [
 path('line-reg/', views.linear_regression, name='line-reg')
]