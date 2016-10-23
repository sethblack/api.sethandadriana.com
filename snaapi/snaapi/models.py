from django.db import models
from PIL import Image

import datetime
import logging

logger = logging.getLogger(__name__)

class WeddingPicture(models.Model):
    owner = models.CharField(max_length=64)
    upload_date = models.DateTimeField(auto_now_add=True)
    capture_date = models.DateTimeField(null=True, blank=True, default=None)
    picture = models.ImageField(upload_to='weddingpictures/%Y/%m/%d/')
    approved = models.BooleanField(default=True)

    def get_date_taken(self):
        try:
            exif_time = Image.open(self.picture.path)._getexif()[36867]
        except:
            return None

        parsed_date_time = None

        try:
            parsed_date_time = datetime.datetime.strptime(exif_time, '%Y:%m:%d %H:%M:%S')
        except:
            pass

        return parsed_date_time

    def save(self, *args, **kwargs):
        super(WeddingPicture, self).save(*args, **kwargs)

        if self.picture:
            self.capture_date = self.get_date_taken()
            super(WeddingPicture, self).save(*args, **kwargs)


class UploadCode(models.Model):
    code = models.CharField(max_length=24)
    full_name = models.CharField(max_length=64)