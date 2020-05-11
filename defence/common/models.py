from django.db import models

# Create your models here.

class app(models.Model):
 
    app_name=models.TextField()
    group_id=models.TextField()