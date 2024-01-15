from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.views import generic
#from .forms import EditSettingsForm, EditPasswordForm  # Import your custom forms

from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView
from storages.backends.s3boto3 import S3Boto3Storage

from Blogs.models import Post
from Homepage.forms import NoteForm
from Homepage.models import Note
from Members.forms import SignUpForm, EditSettingsForm, EditPasswordForm
from Members.models import Profile

'''
from MainApp.forms import NoteForm
from MainApp.models import Profile, Note, Post
from django import forms
from MainApp.models import Profile
from .forms import SignUpForm, ProfilePageForm, EditPasswordForm, EditSettingsForm
'''

class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'members/edit_profile_page.html'
    fields = ['bio', 'github_url', 'linkedin_url', 'academic_field', 'profile_picture']
    success_url = reverse_lazy('MainApp:home')


def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'profile_list.html', {"profiles": profiles})

def econ_profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'econ_profile_list.html', {"profiles": profiles})

def polisci_profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'polisci_profile_list.html', {"profiles": profiles})

def medicine_profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'medicine_profile_list.html', {"profiles": profiles})

class CreateProfileView(CreateView):
    model = Profile
    fields = ['bio', 'github_url', 'linkedin_url', 'academic_field', 'profile_picture']
    template_name = "members/create_profile.html"

    # fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


'''class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')'''


'''def UserRegisterView(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'members/register.html', {'form': form})

def UserLoginView(request):
    return render(request, 'members/login.html')'''
def custom_user_registration_view(request):
    template_name = 'registration/register.html'
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')  # Change 'home' to the name of your home view
    return render(request, template_name, {'form': form})

def custom_user_login_view(request):
    template_name = 'registration/login.html'
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  # Change 'home' to the name of your home view
    else:
        form = AuthenticationForm(request)
    return render(request, template_name, {'form': form})

class UserEditView(generic.UpdateView):
    template_name = 'edit_profile.html'
    form_class = EditSettingsForm  # Use the custom form for user information
    success_url = reverse_lazy('MainApp:home')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = EditPasswordForm()  # Use the custom password change form
        return context

    def form_valid(self, form):
        user = form.save()
        password_form = self.request.POST.get('password_form', '')  # Default to empty string if not present
        new_password1 = self.request.POST.get('new_password1', '')
        new_password2 = self.request.POST.get('new_password2', '')

        if password_form == 'password_change' and new_password1 and new_password2:
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(self.request, user)  # Keep the user logged in
                messages.success(self.request, 'Password changed successfully.')
            else:
                messages.error(self.request, 'New passwords do not match.')

        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)


'''class ProfileView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def post(self, request, pk):
        print("pk =",pk)
        if request.user.is_authenticated:
            profile = Profile.objects.get(user_id=pk)

            if request.method == "post":
                current_user_profile = request.user.profile
                action = request.POST['follow']

                if action == 'unfollow':
                    current_user_profile.follows.remove(profile)
                else:
                    current_user_profile.follows.add(profile)
                current_user_profile.save()

            return render(request, 'registration/user_profile.html', {'profile': profile})
        else:
            return redirect('MainApp:home')
    login_url = 'MainApp:home' 

    def get(self, request, pk):
        profile = Profile.objects.get(user_id=pk)
        return render(request, 'registration/user_profile.html', {'profile': profile})

    def post(self, request, pk):
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST.get('follow')

            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            else:
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return redirect('ProfileView', pk=pk)

    def get_context_data(self, *args, **kwargs):
        cat_menu = Profile.objects.all()
        context = super(ProfileView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

        context["page_user"] = page_user
        return context'''


def ProfileView(request, pk):
    if request.user.is_authenticated:
        form = NoteForm(request.POST or None)
        profile = Profile.objects.get(id=pk)
        followed_profiles = request.user.profile.follows.all()
        note = Note.objects.filter(profile__in=followed_profiles)

        # Get the academic field of the profile
        academic_field = profile.academic_field

        # Filter the posts based on academic field and author
        posts = Post.objects.filter(author=profile.user, category__category=academic_field)

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']

            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return render(request, 'members/user_profile.html', {'profile': profile, 'note': note, 'form': form, 'posts': posts})
    else:
        return redirect('MainApp:home')


    '''requested_url = request.path
    if request.user.is_authenticated:
        form = NoteForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                note = form.save(commit=False)
                note.profile = request.user.profile
                note.user = request.user
                note.save()
                return redirect('MainApp:home')

        followed_profiles = request.user.profile.follows.all()
        print("FOLLOWING: ", followed_profiles)
        current_user = request.user
        print("URL is......", requested_url)
        home = Post.published.all()
        notes = Note.objects.filter(profile__in=followed_profiles)
        # notes = Note.objects.all().order_by("-created_at")
        paginator = Paginator(home, 2)
        page_number = request.GET.get('page', 1)
        # notes = Note.objects.all()
        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            # if page_number not an int, display first page
            posts = paginator.page(1)
        except EmptyPage:
            # If page_number out of range, display last page of results
            posts = paginator.page(paginator.num_pages)
        if requested_url == "/MainApp/philosophy/":
            return render(request, 'MainApp/post/philosophy_blog.html', {'posts': posts})
        elif requested_url == "/MainApp/economics/":
            return render(request, 'MainApp/post/economics.html', {'posts': posts})
        else:
            return render(request, 'MainApp/post/list.html', {'notes': notes, "form": form})
    else:
        return render(request, 'MainApp/post/list.html')'''