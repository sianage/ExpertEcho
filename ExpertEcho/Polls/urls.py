from django.urls import path
from . import views
urlpatterns = [
    path('economics_polls/', views.economics_polls, name='economics_poll_list'),
    path('finance_polls/', views.finance_polls, name='finance_poll_list'),
    path('law_polls/', views.law_polls, name='law_poll_list'),
    path('medicine_polls/', views.medicine_polls, name='medicine_poll_list'),
    path('polls/<category>/', views.polls_by_category, name='poll_list_by_category'),
    path('poll_details/<int:poll_id>/', views.poll_detail, name='poll_details'),
    path('polls/vote/<int:poll_id>/', views.vote, name='vote'),
    path('polls/results/<int:poll_id>/', views.results, name="results"),
    path('create_poll', views.CreatePollView, name='create_poll')
]