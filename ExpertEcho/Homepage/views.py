from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

import Blogs
from Blogs.models import Post
from Debates.models import Debate
from Homepage.forms import NoteForm
from .models import Note
from Members.models import Profile
from django.core.paginator import Paginator

from django.utils import timezone
from itertools import chain
from operator import attrgetter

def about(request):
    return render(request, 'homepage/about.html')


from django.http import JsonResponse
from django.core.paginator import Paginator
from itertools import chain

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


def format_item(item, item_type):
    if item_type == 'blog':
        date_field = item.publish
    else:
        date_field = item.created

    url_method = getattr(item, 'get_absolute_url', None)
    url = url_method() if url_method else "No URL method"
    if url_method:
        url = url_method()
    else:
        if item_type == 'note':
            url = f'/note/{item.id}/'
        elif item_type == 'blog':
            url = f'/blog/{item.id}/'
        elif item_type == 'debate':
            url = f'/debate/{item.id}/'

    print(f"URL for item {getattr(item, 'title', 'No Title')}: {url}")

    base_info = {
        "type": item_type,
        "id": item.id,
        "title": getattr(item, 'title', None),
        "created": date_field.strftime("%Y-%m-%d %H:%M:%S"),
        "profile_picture": item.author_profile.profile_picture.url if item.author_profile.profile_picture else None,
        "first_name": item.author_profile.first_name,
        "last_name": item.author_profile.last_name,
        "email": item.author_profile.user.email,
        "url": url
    }

    if item_type == 'note':
        base_info['body'] = item.body

    return base_info




def home(request):
    if not request.user.is_authenticated:
        return render(request, 'homepage/homepage.html')

    form = NoteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        note = form.save(commit=False)
        note.author_profile = request.user.profile
        note.user = request.user
        note.save()
        return redirect('home')

    try:
        profile = request.user.profile
        followed_profiles = profile.follows.all()

        notes = Note.objects.filter(author_profile__in=followed_profiles).order_by("-created")
        blogs = Post.published.filter(author_profile__in=followed_profiles).order_by("-publish")
        debates = Debate.objects.filter(author_profile__in=followed_profiles).order_by("-created")

        note_list = [format_item(item, 'note') for item in notes]
        blog_list = [format_item(item, 'blog') for item in blogs]
        debate_list = [format_item(item, 'debate') for item in debates]

        note_paginator = Paginator(note_list, 10)
        blog_paginator = Paginator(blog_list, 10)
        debate_paginator = Paginator(debate_list, 10)

        page_number = request.GET.get('page')
        tab = request.GET.get('tab', 'notes')

        if tab == 'notes':
            page_obj = note_paginator.get_page(page_number)
            total_items = len(note_list)
        elif tab == 'blogs':
            page_obj = blog_paginator.get_page(page_number)
            total_items = len(blog_list)
        elif tab == 'debates':
            page_obj = debate_paginator.get_page(page_number)
            total_items = len(debate_list)
        else:
            page_obj = note_paginator.get_page(page_number)
            total_items = len(note_list)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "items": list(page_obj),
                "has_next": page_obj.has_next()
            })

        return render(request, 'homepage/homepage.html', {
            'page_obj': page_obj,
            "form": form,
            "tab": tab,
            "total_items": total_items
        })
    except ObjectDoesNotExist as e:
        print("Error:", e)
        return redirect("create_profile_page")
    except Exception as e:
        print("Unhandled Error:", e)
        return JsonResponse({'error': str(e)}, status=500)








def delete_note(request, pk):
    if request.user.is_authenticated:
        note = get_object_or_404(Note, id=pk)
        # Check if user owns note
        if request.user.profile == note.author_profile:
            note.delete()
            # messages
            print("Note Deleted")
            return redirect('home')
        else:
            # messages
            print("Not your note")
            return redirect("home")

def edit_note(request, pk):
    if request.user.is_authenticated:
        note = get_object_or_404(Note, id=pk)
        if request.user.profile == note.author_profile:
            form = NoteForm(request.POST or None, instance=note)
            if request.method == "POST":
                if form.is_valid():
                    note = form.save(commit=False)
                    note.author_profile = request.user.profile
                    note.user = request.user
                    note.save()
                    print("Note edited")
                    return redirect('home')
                else:
                    print("Error in form")
            return render(request, 'homepage/edit_note.html', {'form': form, 'note': note})
        else:
            print("Not your note")
            return redirect('home')
    else:
        return redirect('home')