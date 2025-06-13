from django.shortcuts import render, redirect
from django.contrib import messages
from uploading_and_processing_file.models import UploadedFile
import csv
import io

def is_valid_csv_for_analysis(content_io):
  reader = csv.reader(content_io)
  rows = list(reader)

  if not rows:
    return False, "File is empty."

  headers = rows[0]
  num_cols = len(headers)

  if any(h.strip() == "" for h in headers):
    return False, "The file contains empty headers."

  for i, row in enumerate(rows[1:], start=2):
    if len(row) != num_cols:
      return False, "The file contains rows in which number of columns does not match the number of headers."

  has_data = any(any(cell.strip() != "" for cell in row) for row in rows[1:])
  if not has_data:
    return False, "The file contains no data except of header."

  return True, None

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
            content.seek(0)
            is_valid, error_message = is_valid_csv_for_analysis(content)

            if not is_valid:
              alert_class = 'danger'
              message = error_message

            else:
              existing_file = UploadedFile.objects.filter(file='uploads/' + uploaded_file.name).first()
              if existing_file:
                existing_file.file.delete(save=False)
                existing_file.file = uploaded_file
                existing_file.save()
                request.session['uploaded_file_id'] = existing_file.id
                message = "Existing file replaced successfully. Now you can move on to the next step."
                alert_class = "success"
              else:
                new_file = UploadedFile(file=uploaded_file)
                new_file.save()
                request.session['uploaded_file_id'] = new_file.id
                message = "File uploaded and saved successfully. Now you can move on to the next step."
                alert_class = "success"

          except Exception as exception:
            alert_class = 'danger'
            message = 'Error occurred during processing csv file: ', str(exception)
  else:
    return render(request, 'analysis_page.html')
  
  return render(request, 'analysis_page.html', {'alert_class': alert_class, 'message': message})