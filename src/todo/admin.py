from django.contrib import admin

from todo.models import CustomUser, Todo

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
    ]

    search_fields = ['username']

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'date',
    ]

    search_fields = ['title']
    
