from django.db import models


# Create your models here.
class registration(models.Model):

    firmname=models.CharField(max_length=100)
    firmhead=models.CharField(max_length=100)
    addr=models.TextField()
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    # doc = models.FileField(upload_to="firm_uploads")
    doc = models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    region=models.CharField(max_length=100)
    remarks=models.CharField(max_length=300,null=True, blank=True)
    request_date=models.TextField()
    extension=models.CharField(max_length=30)

