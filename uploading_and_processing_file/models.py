from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):

  file = models.FileField(upload_to='uploads/') 
  uploaded_time = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.file.name

