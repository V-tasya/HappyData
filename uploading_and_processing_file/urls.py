from django.urls import path
from uploading_and_processing_file import views

app_name = 'upload'
urlpatterns = [
 path('process-csv/', views.process_csv, name='process_csv')
]