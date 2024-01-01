from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import UpdateBlogView, DeleteBlogView, user_blogs, philosophy_view, medicine_view, polisci_view, economics_view, AddBlogView, post_detail

urlpatterns = [
    path('philosophy/', views.philosophy_view, name='philosophy_blog_list'),
    path('user_blogs/', user_blogs.as_view(), name='user_blogs'),
    path('economics/', views.economics_view, name='economics_blog_list'),
    path('polisci/', views.polisci_view, name='polisci_blog_list'),
    path('medicine/', views.medicine_view, name='medicine_blog_list'),
    path('blog_post/<int:pk>/', post_detail.as_view(), name='post_detail'),
    path('add_post/', AddBlogView.as_view(), name="add_post"),
    path('blog_post/edit/<int:pk>', UpdateBlogView.as_view(), name='update_post'),
    path('blog_post/delete/<int:pk>', DeleteBlogView.as_view(), name='delete_post'),
    path('draft_list/', views.DraftListView.as_view(), name='draft_list'),
]