from django.contrib import admin
from .models import Organization
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
admin.site.register(Organization)
admin.site.register(User, UserAdmin)
