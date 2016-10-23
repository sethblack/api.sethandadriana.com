from django.db import models

class WeddingPicture(models.Model):
    owner = models.CharField(max_length=64)
    upload_date = models.DateTimeField(auto_now_add=True)
    capture_date = models.DateTimeField()
    picture = models.ImageField(upload_to='weddingpictures/%Y/%m/%d/')
    approved = models.BooleanField(default=True)


class UploadCode(models.Model):
    code = models.CharField(max_length=24)
    full_name = models.CharField(max_length=64)