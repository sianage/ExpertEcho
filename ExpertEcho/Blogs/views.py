from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect

from Members.models import Profile
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
from .models import Post, CustomUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from fields import FIELD_CHOICES
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
    model = Post
    template_name = 'blogs/user_blogs.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        if author_id:
            # Retrieve the author's profile using the provided author_id
            author_profile = get_object_or_404(Profile, id=author_id)
            # Use the related_name 'blog_posts' to filter posts by this profile
            return Post.objects.filter(author_profile=author_profile)
        else:
            return Post.objects.all()


'''class blog_list(ListView):
    model = Post
    template_name = 'blogs/tech_blogs.html'

    def get_queryset(self):
        # Filter posts by the "technology" category
        return Post.objects.filter(category="Field5")'''
from django.db.models import Prefetch

class blog_list(ListView):
    model = Post
    template_name = 'blogs/blog_list.html'

    def get_category_name(self, field_identifier):
        # Convert field identifier to human-readable name
        return dict(FIELD_CHOICES).get(field_identifier, "Unknown Category")

    def get_queryset(self):
        category = self.kwargs['category']
        queryset = Post.objects.filter(category=category).select_related('author_profile')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_identifier = self.kwargs['category']
        # Use the new method to get the category name and pass it to the template
        context['category_name'] = self.get_category_name(category_identifier)
        return context

    '''def get_queryset(self):
        queryset = Post.objects.filter(category="Field5").select_related('author_profile')

        for post in queryset:
            author = post.author_profile.user
            # Since the Profile is directly linked to CustomUser and we've already fetched it with select_related
            profile = author.profile
            if profile.profile_picture:
                print(f"Profile Picture URL: {profile.profile_picture.url}")
            else:
                print("No profile picture.")

            print("-" * 40)  # Print a separator for readability

        return queryset'''


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
        form.instance.category = academic_field

        return super().form_valid(form)

class DeleteBlogView(DeleteView):
    model = Post
    template_name = 'blogs/delete_blog.html'
    success_url = reverse_lazy('home')


class AddBlogView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blogs/add_blog.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Set the author of the post to the currently logged-in user
        form.instance.author_profile = self.request.user.profile

        # Capitalize the first letter of the academic_field and set it as the category name
        academic_field = self.request.user.profile.academic_field.capitalize()
        form.instance.category = academic_field
        print("Author Profile User ID:", form.instance.author_profile.user.id)

        return super().form_valid(form)

class post_detail(DetailView, ):
    model = Post
    template_name = 'blogs/blog_detail.html'
    success_url = reverse_lazy('post_detail')