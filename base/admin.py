from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Teacher)
admin.site.register(Assignment)
admin.site.register(Event)
admin.site.register(Schedule)
admin.site.register(MyClasses)
admin.site.register(Announcement)