from django.contrib import admin
from django.contrib.auth.admin  import UserAdmin
from .models import User

# Register your models here.

# change UserAdmin fields and append some fields
UserAdmin.fieldsets[1][1]['fields'] = ('first_name', 'last_name', 'email', 'phone', 'is_access')
UserAdmin.list_display = ('username', 'email', 'phone', 'first_name', 'last_name', 'is_staff', 'is_access')
# and register our custorm user model and UserAdmin
admin.site.register(User, UserAdmin)