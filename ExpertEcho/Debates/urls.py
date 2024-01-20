from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from Blogs.views import (UpdateBlogView, DeleteBlogView, user_blogs, philosophy_view, medicine_view,
                                    polisci_view, economics_view, AddBlogView, post_detail)
from .views import user_debate_list, debate_list, economics_debate_list, polisci_debate_list, medicine_debate_list, \
    debate_detail, AddDebateView

urlpatterns = [
    path('debates/user_debate_list/', user_debate_list.as_view(), name='user_debates'),
    path('debates/debate_list/', debate_list.as_view(), name='debate_list'),
    path('debates/economics_debate_list/', economics_debate_list.as_view(), name='economics_debate_list'),
    path('debates/polisci_debate_list/', polisci_debate_list.as_view(), name='polisci_debate_list'),
    path('debates/medicine_debate_list/', medicine_debate_list.as_view(), name='medicine_debate_list'),
    path('debates/debate/<int:pk>/', debate_detail.as_view(), name='debate-details'),
    path('debates/debate/<int:pk>/comment/', views.AddCommentView, name="comment"),
    path('debates/start_debate/', AddDebateView.as_view(), name="start_debate"),
]