from django.contrib import admin
from django.urls import path, include

from .views import index, remove, add_task, modify_task

app_name = 'todo'

urlpatterns = [
    path('', index, name='index'),
    path('ajouter-tache/', add_task, name='add_task'),
    path('modifier-tache/<int:task_id>', modify_task, name='modify_task'),
    path('supprimer-task/<int:task_id>', remove, name='remove'),
]
