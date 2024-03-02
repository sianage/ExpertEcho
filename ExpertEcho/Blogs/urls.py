from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import UpdateBlogView, DeleteBlogView, user_blogs, blog_list, medicine_view, polisci_view, economics_view, AddBlogView, post_detail

urlpatterns = [
    path('blogs/<category>/', blog_list.as_view(), name='blog_list_by_category'),
    path('user_blogs/', user_blogs.as_view(), name='user_blogs'),
    path('blogs/blog_post/<int:pk>/', post_detail.as_view(), name='post_detail'),
    path('blogs/create_blog/', AddBlogView.as_view(), name="create_post"),
    path('blogs/blog_post/edit/<int:pk>', UpdateBlogView.as_view(), name='update_post'),
    path('blogs/blog_post/delete/<int:pk>', DeleteBlogView.as_view(), name='delete_post'),
    path('blogs/draft_list/', views.DraftListView.as_view(), name='draft_list'),
]