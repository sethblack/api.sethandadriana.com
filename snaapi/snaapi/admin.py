from django.contrib import admin
from snaapi import models


class UploadCodeAdmin(admin.ModelAdmin):
    model = models.UploadCode
    list_display = ('code', 'full_name', )


class WeddingPictureAdmin(admin.ModelAdmin):
    model = models.WeddingPicture
    list_display = ('owner', 'upload_date', 'picture', )


admin.site.register(models.UploadCode, UploadCodeAdmin)
admin.site.register(models.WeddingPicture, WeddingPictureAdmin)