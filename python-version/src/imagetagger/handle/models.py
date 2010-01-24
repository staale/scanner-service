from django.db import models

from datetime import datetime

class ImageFile(models.Model):
    path = models.CharField(max_length=150)
    scan_date = models.DateField(default=datetime.now)
#    scanned_image = models.ForeignKey("ScannedImage", null=True)

class ScannedImage(models.Model):
    original = models.OneToOneField(ImageFile)
    source = models.CharField(max_length=150)
    description = models.CharField(max_length=500)

class ImageTag(models.Model):
    scanned_image = models.ForeignKey(ScannedImage)
    tag = models.CharField(max_length=150, db_index=True)