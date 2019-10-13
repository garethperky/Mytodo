from django.contrib import admin

from .models import Todo, UserProfile


class TodoAdmin(admin.ModelAdmin):
      list_display = ('title', 'description', 'completed')

class User_Profile(admin.ModelAdmin):
      list_display = ('user', 'image')

admin.site.register(Todo, TodoAdmin)
admin.site.register(UserProfile, User_Profile)
