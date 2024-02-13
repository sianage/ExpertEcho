from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.custom_user_login_view, name="login"),
    path('register/', views.custom_user_registration_view, name="register"),
    path('edit_settings/', views.edit_settings_view, name="edit_settings"),
    path('profile/<int:pk>/', views.profile_view, name="profile_page"),
    path('create_profile/', views.create_profile_view, name="create_profile_page"),
    path('edit_profile/<int:pk>/', views.edit_profile_view, name="edit_profile_page"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('econ_profile_list/', views.econ_profile_list, name='econ_profile_list'),
    path('polisci_profile_list/', views.polisci_profile_list, name='polisci_profile_list'),
    path('medicine_profile_list/', views.medicine_profile_list, name='medicine_profile_list'),
    path('conversations/<int:receiver_id>/', views.private_message_view, name='conversation_detail'),
]