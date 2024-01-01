from django.urls import path
from . import views
from .views import philosophy_poll_list, poll_detail, economics_poll_list, polisci_poll_list, medicine_poll_list
urlpatterns = [
    path('philosophy_poll_list/', philosophy_poll_list.as_view(), name='philosophy_poll_list'),
    path('economics_poll_list/', economics_poll_list.as_view(), name='economics_poll_list'),
    path('polisci_poll_list/', polisci_poll_list.as_view(), name='polisci_poll_list'),
    path('medicine_poll_list/', medicine_poll_list.as_view(), name='medicine_poll_list'),
    path('<int:poll_id>/poll_details/', views.poll_detail, name='poll_details'),
    path('<int:poll_id>/vote/', views.vote, name='vote'),
    path('<int:poll_id>/results/', views.results, name="results"),
    path('create_poll', views.CreatePollView, name='create_poll')
]