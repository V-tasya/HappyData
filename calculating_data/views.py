import pandas as pd
from django.shortcuts import render
from uploading_and_processing_file.models import UploadedFile
from django.http import JsonResponse
import json

def basic_data(request):
  if request.method == "POST":
    file_id = request.session.get('uploaded_file_id')
    data = {}

    if not file_id:
      comment = "Upload file."
      data['mess1'] = comment
      return JsonResponse(data)
    
    try:
      up_file = UploadedFile.objects.get(id=file_id)
      data_frame = pd.read_csv(up_file.file.path)
      data['file_name_inp'] = up_file.file.name.split('/')[-1]
      data['number_of_col'] = data_frame.shape[1]
      data['number_of_rows'] = data_frame.shape[0]
      data['number_of_num_val'] = data_frame.select_dtypes(include='number').shape[1]
      data['number_of_cat_val'] = data_frame.select_dtypes(exclude='number').shape[1]
      data['number_of_miss_val'] = int(data_frame.isnull().sum().sum())
      data['mess1'] = 'Filled'
    except Exception as error:
      message = 'Ups, something goes wrong'
      data['mess1'] = message
      print(error)
      return JsonResponse(data)
   
    return JsonResponse(data)
  
def get_numeric_columns(request):
  if request.method == "POST":
    file_id = request.session.get('uploaded_file_id')
    data = {}

    if not file_id:
      comment = "Upload file."
      data['mess2'] = comment
      return JsonResponse(data)
        
    try:
      up_file = UploadedFile.objects.get(id=file_id)
      data_frame = pd.read_csv(up_file.file.path)
      num_cols = data_frame.select_dtypes(include='number').columns.tolist()
      data['numeric_columns'] = num_cols
      return JsonResponse(data)
        
    except Exception as error:
      message = 'Ups, something goes wrong'
      data['mess2'] = message
      print(error)
      return JsonResponse(data)
    
  return JsonResponse({'error': 'Invalid request method'}, status=400)

def calculate_data(request):
  if request.method == "POST":
    file_id = request.session.get('uploaded_file_id')
    if not file_id:
      return JsonResponse({'error': 'Upload file first.'})

    try:
      up_file = UploadedFile.objects.get(id=file_id)
      data_frame = pd.read_csv(up_file.file.path)

      body = json.loads(request.body)
      column_name = body.get("column")

      if column_name not in data_frame.columns:
        return JsonResponse({'error': 'Column not found.'})

      if not pd.api.types.is_numeric_dtype(data_frame[column_name]):
        return JsonResponse({'error': 'Selected column is not numeric.'})

      col = data_frame[column_name].dropna()

      result = {
        "mean_val": round(float(col.mean()), 2),
        "median_val": round(float(col.median()), 2),
        "std_val": round(float(col.std()), 2),
        "mess2": "Calculated"
      }
      return JsonResponse(result)
    except Exception as error:
      print(error)
      return JsonResponse({'err': 'Something went wrong.'})

  return JsonResponse({'err': 'Invalid request method.'}, status=400)