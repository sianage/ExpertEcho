from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from .forms import PostForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, request
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from .models import Post
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, CreateView
from .models import Post, Category, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST

# Helper function to get posts by category and paginate them
def get_category_posts(category_name, request):
    home = Post.published.all().filter(category__category=category_name)
    paginator = Paginator(home, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts
class DraftListView(LoginRequiredMixin, ListView):
    template_name = 'blogs/blog_draft_list.html'
    context_object_name = 'draft_posts'

    def get_queryset(self):
        # Retrieve draft posts authored by the currently logged-in user
        return Post.objects.filter(author=self.request.user, status=Post.Status.DRAFT)

    def get_post_detail_url(self, post):
        return reverse('post_detail', kwargs={'pk': post.pk})


class user_blogs(ListView):
    print("blog list")
    model = Post
    template_name = 'blogs/user_blogs.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Post.objects.filter(author_id=author_id)
        else:
            return Post.objects.all()

def philosophy_view(request):
    # Logic for the philosophy section
    posts = get_category_posts("Philosophy", request)
    return render(request, 'blogs/philosophy_blogs.html', {'posts': posts})

def economics_view(request):
    # Logic for the economics section
    posts = get_category_posts("Economics", request)
    return render(request, 'blogs/economics_blogs.html', {'posts': posts})

def medicine_view(request):
    # Logic for the medicine section
    posts = get_category_posts("Medicine", request)
    return render(request, 'blogs/medicine_blogs.html', {'posts': posts})

def polisci_view(request):
    # Logic for the political science section
    posts = get_category_posts("Political Science", request)
    return render(request, 'blogs/political_science_blogs.html', {'posts': posts})

class UpdateBlogView(UpdateView):
    model = Post
    template_name = 'blogs/update_blog.html'
    fields = ['title', 'body', 'status']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Set the author of the post to the currently logged-in user
        form.instance.author = self.request.user

        # Capitalize the first letter of the academic_field and set it as the category name
        academic_field = self.request.user.profile.academic_field.capitalize()
        category, _ = Category.objects.get_or_create(category=academic_field)
        form.instance.category = category

        return super().form_valid(form)

class DeleteBlogView(DeleteView):
    model = Post
    template_name = 'blogs/delete_blog.html'
    success_url = reverse_lazy('philosophy_blog_list')

    class AddBlogView(LoginRequiredMixin, CreateView):
        model = Post
        form_class = PostForm
        template_name = 'blogs/add_post.html'
        success_url = reverse_lazy('home')

        def form_valid(self, form):
            # Set the author of the post to the currently logged-in user
            form.instance.author = self.request.user

            # Capitalize the first letter of the academic_field and set it as the category name
            academic_field = self.request.user.profile.academic_field.capitalize()
            category, _ = Category.objects.get_or_create(category=academic_field)
            form.instance.category = category

            return super().form_valid(form)

class AddBlogView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'MainApp/post/add_post.html'
    success_url = reverse_lazy('MainApp:home')

    def form_valid(self, form):
        # Set the author of the post to the currently logged-in user
        form.instance.author = self.request.user

        # Capitalize the first letter of the academic_field and set it as the category name
        academic_field = self.request.user.profile.academic_field.capitalize()
        category, _ = Category.objects.get_or_create(category=academic_field)
        form.instance.category = category

        return super().form_valid(form)

class post_detail(DetailView, ):
    model = Post
    template_name = 'MainApp/post/detail.html'
    success_url = reverse_lazy('post_detail')