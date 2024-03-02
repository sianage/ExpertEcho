from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete_note/<int:pk>', views.delete_note, name='delete_note'),
    path('edit_note/<int:pk>', views.edit_note, name='edit_note'),
]