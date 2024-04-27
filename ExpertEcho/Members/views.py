from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.views import generic
#from .forms import EditSettingsForm, EditPasswordForm  # Import your custom forms

from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView, CreateView
from storages.backends.s3boto3 import S3Boto3Storage

from Blogs.models import Post
from Homepage.forms import NoteForm
from Homepage.models import Note
from Members.forms import SignUpForm, EditSettingsForm, EditProfileForm, CreateProfileForm, \
    CustomUserCreationForm, MessageForm, EditPasswordForm
from Members.models import Profile, CustomUser, CustomUserManager, Message
from fields import FIELD_CHOICES


@login_required
def edit_profile_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    # Ensure the user editing the profile is the profile owner
    if profile.user != request.user:
        messages.error(request, "You do not have permission to edit this profile.")
        return redirect('some_error_handling_view')

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('home')  # Ensure you're using the correct path or name for your home view
        else:
            # Form is not valid, handle form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            # Re-render the form with errors
            return render(request, 'members/edit_profile.html', {'form': form})
    else:
        form = EditProfileForm(instance=profile, user=request.user)

    return render(request, 'members/edit_profile.html', {'form': form})



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

@login_required
def create_profile_view(request):
    if request.method == 'POST':
        form = CreateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully.')
            return redirect('home')
    else:
        form = CreateProfileForm()

    return render(request, 'members/create_profile.html', {'form': form})


import logging

logger = logging.getLogger(__name__)

def custom_user_registration_view(request):
    template_name = 'registration/register.html'
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info('Redirecting to homepage after registration.')
            return redirect('home')
        else:
            logger.error('Form is not valid. Errors: %s', form.errors)
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

@login_required
def edit_settings_view(request):
    if request.method == 'POST':
        form = EditSettingsForm(request.POST, instance=request.user)
        password_form = EditPasswordForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password_change = request.POST.get('password_change', '')  # Correct the field name
            new_password1 = request.POST.get('new_password1', '')
            new_password2 = request.POST.get('new_password2', '')

            if password_change == 'password_change' and new_password1 and new_password2:
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    update_session_auth_hash(request, user)  # Keep the user logged in
                    messages.success(request, 'Password changed successfully.')
                    return redirect('home')
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                # Remove the unnecessary save here
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('home')
    else:
        form = EditSettingsForm(instance=request.user)
        password_form = EditPasswordForm()

    context = {
        'form': form,
        'password_form': password_form,
    }
    return render(request, 'members/edit_settings.html', context)



def profile_view(request, pk):

    profile = Profile.objects.get(id=pk)

    print(f"Debug: Profile ID = {profile.id}, User ID = {profile.user.id}")  # Debug print
    # Rest of your code...
    if request.user.is_authenticated:
        form = NoteForm(request.POST or None)
        profile = Profile.objects.get(id=pk)
        followed_profiles = request.user.profile.follows.all()
        note = Note.objects.filter(author_profile__in=followed_profiles)

        # Get the academic field of the profile
        academic_field = profile.academic_field

        # Filter the posts based on academic field and author
        #posts = Post.objects.filter(author_profile=profile, category=academic_field)

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']

            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return render(request, 'members/profile.html', {'profile': profile, 'note': note, 'form': form})
    else:
        return redirect('home')

@login_required
def private_message_view(request, receiver_id):
    receiver = get_object_or_404(CustomUser, id=receiver_id)
    sender = request.user

    # Check if the current user is part of the conversation
    if sender != receiver and not Message.objects.filter(
        (Q(sender=sender) & Q(receiver=receiver)) |
        (Q(sender=receiver) & Q(receiver=sender))
    ).exists():
        # If the check fails, return a Forbidden response
        return HttpResponseForbidden("You are not allowed to view this conversation.")

    messages = Message.objects.filter(
        (Q(sender=sender) & Q(receiver=receiver)) |
        (Q(sender=receiver) & Q(receiver=sender))
    ).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.receiver = receiver
            message.save()
            return redirect('message', receiver_id=receiver_id)
    else:
        form = MessageForm()

    return render(request, 'members/message.html', {'receiver': receiver, 'messages': messages, 'form': form})

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(CustomUser, id=receiver_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()

            # Redirect to the conversation_detail view with the correct receiver_id
            return redirect('message', receiver_id=receiver_id)
    else:
        form = MessageForm()

    return render(request, 'members/message.html', {'receiver': receiver, 'form': form})

def expert_list(request, field):
    # Convert field identifier to human-readable name
    field_name = dict(FIELD_CHOICES).get(field, "Unknown Field")

    # Retrieve search term from GET request
    search_query = request.GET.get('search', '')

    profiles = Profile.objects.filter(academic_field=field)  # Base query

    if search_query:
        name_parts = search_query.split()

        # If the search query includes both first and last names
        if len(name_parts) > 1:
            profiles = profiles.filter(
                Q(first_name__icontains=name_parts[0]),
                Q(last_name__icontains=name_parts[-1])
            )
        else:
            # Apply the search query to both first and last names if only one part is provided
            profiles = profiles.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )

    return render(request, 'members/expert_list.html', {'profiles': profiles, 'field_name': field_name})

@login_required
def conversation_list(request):
    user = request.user
    conversations = CustomUser.objects.exclude(id=user.id)

    conversations_with_messages = []
    for conversation in conversations:
        has_sent_messages = Message.objects.filter(sender=user, receiver=conversation).exists()
        has_received_messages = Message.objects.filter(sender=conversation, receiver=user).exists()

        if has_sent_messages or has_received_messages:
            conversations_with_messages.append(conversation)

    return render(request, 'members/conversations.html', {'conversations': conversations_with_messages})
