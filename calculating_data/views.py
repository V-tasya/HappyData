from django.shortcuts import render,redirect
from uploading_and_processing_file.models import UploadedFile

def basic_info(request):
  message = ''
  file_name = None

  if request.method == 'POST':
    file_id = request.session.get('uploaded_file_id')
    if not file_id:
      message = "Nither of files have been uploaded."
      return redirect('analysis_page.html', {'mess1': message})

  try:
    uploaded_file = UploadedFile.objects.get(id=file_id)
    file_name = uploaded_file.file.name
  except UploadedFile.DoesNotExist:
    message = "Probably the file was deleted."
    return redirect('analysis_page.html', {'mess1': message})
  
  
