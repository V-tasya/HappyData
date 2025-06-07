from django.shortcuts import render, redirect
from django.contrib import messages
from uploading_and_processing_file.models import UploadedFile
import csv
import io

def process_csv(request):
  alert_class = ''
  messages.message = None

  if request.method == 'POST':
    uploaded_file = request.FILES.get('csv_file')

    if not uploaded_file:
      alert_class = 'warning'
      message = 'No file was uploaded. Choose file'
    
    else:
      if not uploaded_file.name.endswith('.csv'):
        alert_class = 'danger'
        message = 'Uploaded file is not a csv file, Choose another file'

      else:
        if uploaded_file.size == 0:
          alert_class = 'warning'
          message = 'Uploaded file is empty. Choose another file'
        
        else:
          try:
            data = uploaded_file.read().decode('utf-8')
            content  = io.StringIO(data)
            csv.reader(content)
            existing_file = UploadedFile.objects.filter(file='uploads/' + uploaded_file.name).first()

            if existing_file:
              existing_file.file.delete(save=False)
              existing_file.file = uploaded_file
              existing_file.save()
              message = "Existing file replaced successfully."
              alert_class = "success"
            else:
              new_file = UploadedFile(file=uploaded_file)
              new_file.save()
              message = "File uploaded and saved successfully."
              alert_class = "success"
          except Exception as exception:
            alert_class = 'danger'
            message = 'Error occurred during processing csv file: ', str(exception)
  else:
    return render(request, 'analysis_page.html')
  
  return render(request, 'analysis_page.html', {'alert_class': alert_class, 'message': message})