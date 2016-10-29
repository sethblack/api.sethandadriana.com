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

def flip_horizontal(im): return im.transpose(Image.FLIP_LEFT_RIGHT)
def flip_vertical(im): return im.transpose(Image.FLIP_TOP_BOTTOM)
def rotate_180(im): return im.transpose(Image.ROTATE_180)
def rotate_90(im): return im.transpose(Image.ROTATE_90)
def rotate_270(im): return im.transpose(Image.ROTATE_270)
def transpose(im): return rotate_90(flip_horizontal(im))
def transverse(im): return rotate_90(flip_vertical(im))
orientation_funcs = [None,
                 lambda x: x,
                 flip_horizontal,
                 rotate_180,
                 flip_vertical,
                 transpose,
                 rotate_270,
                 transverse,
                 rotate_90
                ]

class WeddingPicture(models.Model):
    owner = models.CharField(max_length=64)
    upload_date = models.DateTimeField(auto_now_add=True)
    capture_date = models.DateTimeField(null=True, blank=True, default=None)
    picture = models.ImageField(upload_to='weddingpictures/full/%Y/%m/%d/')
    thumbnail = models.ImageField(upload_to='weddingpictures/thumbs/%Y/%m/%d/', default=None, blank=True, null=True)
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

    def rotate(self):
        fh = storage.open(self.picture.name, 'r')
        try:
            image = Image.open(fh)
        except:
            return False

        image = self.apply_orientation(image)

        # Path to save to, name, and extension
        file_name, file_extension = os.path.splitext(self.picture.name)

        if file_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif file_extension == '.gif':
            FTYPE = 'GIF'
        elif file_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        temp_img = StringIO()
        image.save(temp_img, FTYPE)
        temp_img.seek(0)

        fh.close()

        # Load a ContentFile into the thumbnail field so it gets saved
        self.picture.save(self.picture.name, ContentFile(temp_img.read()), save=False)
        temp_img.close()

    def make_thumbnail(self):
        fh = storage.open(self.picture.name, 'r')
        try:
            image = Image.open(fh)
        except:
            return False

        width, height = image.size

        image = self.apply_orientation(image)

        if width > height:
            image.thumbnail((10000,500), Image.ANTIALIAS)
        else:
            image.thumbnail((600, 10000), Image.ANTIALIAS)

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

    def apply_orientation(self, im):
        """
        Extract the oritentation EXIF tag from the image, which should be a PIL Image instance,
        and if there is an orientation tag that would rotate the image, apply that rotation to
        the Image instance given to do an in-place rotation.

        :param Image im: Image instance to inspect
        :return: A possibly transposed image instance
        """

        try:
            kOrientationEXIFTag = 0x0112
            if hasattr(im, '_getexif'): # only present in JPEGs
                e = im._getexif()       # returns None if no EXIF data
                if e is not None:
                    #log.info('EXIF data found: %r', e)
                    orientation = e[kOrientationEXIFTag]
                    f = orientation_funcs[orientation]
                    return f(im)
        except:
            # We'd be here with an invalid orientation value or some random error?
            pass # log.exception("Error applying EXIF Orientation tag")
        return im

    def save(self, *args, **kwargs):
        super(WeddingPicture, self).save(*args, **kwargs)

        if self.picture:
            if self.capture_date is None:
                self.capture_date = self.get_date_taken()

            self.rotate()

            if len(self.thumbnail) == 0:
                self.make_thumbnail()

            super(WeddingPicture, self).save(*args, **kwargs)


class UploadCode(models.Model):
    code = models.CharField(max_length=24)
    full_name = models.CharField(max_length=64)