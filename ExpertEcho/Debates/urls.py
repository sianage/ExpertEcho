from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from Blogs.views import (UpdateBlogView, DeleteBlogView, user_blogs, medicine_view,
                                    polisci_view, economics_view, AddBlogView, post_detail)
from .views import user_debate_list, debate_list, economics_debate_list, polisci_debate_list, medicine_debate_list, \
    debate_detail

urlpatterns = [
    path('user_debate_list/', user_debate_list.as_view(), name='user_debates'),
    path('debates/<category>/', debate_list.as_view(), name='debate_list_by_category'),
    path('debates/economics_debate_list/', economics_debate_list.as_view(), name='economics_debate_list'),
    path('debates/polisci_debate_list/', polisci_debate_list.as_view(), name='polisci_debate_list'),
    path('debates/medicine_debate_list/', medicine_debate_list.as_view(), name='medicine_debate_list'),
    path('debates/debate/<int:pk>/', debate_detail.as_view(), name='debate_detail'),
    path('debates/debate/<int:pk>/comment/', views.AddCommentView, name="comment"),
    path('start_debate/', views.create_debate, name="start_debate"),
]