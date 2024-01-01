from django.urls import path, include

from . import views
from .views import UserRegisterView, UserEditView, ProfileView, CreateProfileView, EditProfilePageView

#app_name = 'Members'

urlpatterns = [
    path('register/', views.UserRegisterView, name="register"),
    #settings?
    path('edit_profile/', UserEditView.as_view(), name="edit_profile"),
    path('<int:pk>/profile/', views.ProfileView, name="profile_page"),
    path('create_profile/', CreateProfileView.as_view(), name="create_profile_page"),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name="edit_profile_page"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('econ_profile_list/', views.econ_profile_list, name='econ_profile_list'),
    path('polisci_profile_list/', views.polisci_profile_list, name='polisci_profile_list'),
    path('medicine_profile_list/', views.medicine_profile_list, name='medicine_profile_list'),
]