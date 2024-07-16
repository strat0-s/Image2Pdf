from django.db import models

class ImageInstance(models.Model):
    imginst = models.ImageField(blank = False, upload_to='')

    def __str__(self):
        return self.imginst
    
class ImageCollection(models.Model):
    folder_name = models.CharField(max_length=20)
    collection = models.ManyToManyField(ImageInstance)

    def __str__(self):
        return self.folder_name