from django.db import models
from django.utils import timezone
import datetime
import os

class Board(models.Model):
    title           = models.CharField(max_length=250)
    user_id         = models.IntegerField()
    created         = models.DateTimeField(default=timezone.now)
    updated         = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class BoardText(models.Model):
    board           = models.ForeignKey(Board, on_delete=models.CASCADE)
    text            = models.TextField()
    created         = models.DateTimeField(default=timezone.now)
    updated         = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class StickyNotes(models.Model):
    board           = models.ForeignKey(Board, on_delete=models.CASCADE)
    note            = models.TextField()
    created         = models.DateTimeField(default=timezone.now)
    updated         = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.note

class Url(models.Model):
    board           = models.ForeignKey(Board, on_delete=models.CASCADE)
    title           = models.CharField(max_length=250, default="Link to Site")
    url             = models.CharField(max_length=250)
    created         = models.DateTimeField(default=timezone.now)
    updated         = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Image(models.Model):
    board           = models.ForeignKey(Board, on_delete=models.CASCADE)
    title           = models.CharField(max_length=250, default="Picture Title") 
    image           = models.ImageField(upload_to='images/')
    created         = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Video(models.Model):
    board           = models.ForeignKey(Board, on_delete=models.CASCADE) 
    title           = models.CharField(max_length=250, default="Video Title")
    video           = models.FileField(upload_to='videos/')
    created         = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

# reset migrations/db
# https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html