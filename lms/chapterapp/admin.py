from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Chapter)
admin.site.register(LinkChapter)
admin.site.register(TextChapter)
admin.site.register(VideoChapter)
admin.site.register(HeadingChapter)