from django.contrib import admin
from .models import Category, Manufacturer, Project, Asset

# Register your models here.
admin.site.register(Asset)
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Manufacturer)
