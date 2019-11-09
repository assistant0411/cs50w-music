from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='songs/')
    release = models.DateTimeField('Created', auto_now_add=True)