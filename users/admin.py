from django.contrib import admin
from .models import Board, BoardText, StickyNotes, Url, Image, Video

admin.site.register(Board)
admin.site.register(BoardText)
admin.site.register(StickyNotes)
admin.site.register(Url)
admin.site.register(Image)
admin.site.register(Video)
