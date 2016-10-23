from cStringIO import StringIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.db import models
from PIL import Image

import datetime
import logging
import os
import re

logger = logging.getLogger(__name__)

class WeddingPicture(models.Model):
    owner = models.CharField(max_length=64)
    upload_date = models.DateTimeField(auto_now_add=True)
    capture_date = models.DateTimeField(null=True, blank=True, default=None)
    picture = models.ImageField(upload_to='weddingpictures/full/%Y/%m/%d/')
    thumbnail = models.ImageField(upload_to='weddingpictures/thumbs/%Y/%m/%d/', editable=False)
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

    def make_thumbnail(self):
        fh = storage.open(self.picture.name, 'r')
        try:
            image = Image.open(fh)
        except:
            return False

        image.thumbnail((600,500), Image.ANTIALIAS)
        fh.close()

        # Path to save to, name, and extension
        thumb_name, thumb_extension = os.path.splitext(self.picture.name)

        thumb_name = re.sub(r'weddingpictures/full/[\d]+/[\d]+/[\d]+/', '', thumb_name)

        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = StringIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # Load a ContentFile into the thumbnail field so it gets saved
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def save(self, *args, **kwargs):
        super(WeddingPicture, self).save(*args, **kwargs)

        if self.picture:
            self.capture_date = self.get_date_taken()
            self.make_thumbnail()
            super(WeddingPicture, self).save(*args, **kwargs)


class UploadCode(models.Model):
    code = models.CharField(max_length=24)
    full_name = models.CharField(max_length=64)