from django.contrib import admin
from .models import Machine, GcodeFile

admin.site.register(Machine)
admin.site.register(GcodeFile)
