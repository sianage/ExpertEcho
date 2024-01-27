from django.urls import path

from . import views
from .views import custom_user_login_view, ProfileView, custom_user_registration_view, create_profile_view, user_edit_view, edit_profile_page

urlpatterns = [
    path('login/', views.custom_user_login_view, name="login"),
    path('register/', views.custom_user_registration_view, name="register"),
    path('edit_profile/', views.edit_profile_page, name="edit_profile"),
    path('<int:pk>/profile/', views.ProfileView, name="profile_page"),
    path('create_profile/', views.create_profile_view, name="create_profile_page"),
    path('<int:pk>/edit_profile_page/', views.edit_profile_page, name="edit_profile_page"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('econ_profile_list/', views.econ_profile_list, name='econ_profile_list'),
    path('polisci_profile_list/', views.polisci_profile_list, name='polisci_profile_list'),
    path('medicine_profile_list/', views.medicine_profile_list, name='medicine_profile_list'),
]