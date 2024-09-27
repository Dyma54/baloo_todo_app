from django.contrib import admin
from django.urls import path, include

from .views import home

from todo.views import sign_in, sign_out, sign_up

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('todos/', include('todo.urls')),
    path('compte/nouveau', sign_up, name='signup'),
    path('compte/se-connecter/', sign_in, name='login'),
    path('compte/se-deconnecter/', sign_out, name='logout'),
]
