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
    # Determine the appropriate date field
    if item_type == 'blog':
        date_field = item.publish
    else:
        date_field = item.created

    # Initialize base_info dictionary with common attributes
    base_info = {
        "type": item_type,
        "id": item.id,
        "title": getattr(item, 'title', None),
        "created": date_field.strftime("%Y-%m-%d %H:%M:%S"),
        "profile_picture": item.author_profile.profile_picture.url if item.author_profile.profile_picture else None,
        "first_name": item.author_profile.first_name,
        "last_name": item.author_profile.last_name,
        "url": getattr(item, 'get_absolute_url', lambda: None)()
    }

    # Include 'body' attribute if item is a Note
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

        combined_list = [format_item(item, 'note') for item in notes]
        combined_list.extend(format_item(item, 'blog') for item in blogs)
        combined_list.extend(format_item(item, 'debate') for item in debates)

        combined_list = sorted(combined_list, key=lambda x: x['created'], reverse=True)

        paginator = Paginator(combined_list, 10)  # Show 10 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "items": [dict(item, profile_picture=str(item['profile_picture'])) for item in page_obj.object_list],
                "has_next": page_obj.has_next()
            })

        return render(request, 'homepage/homepage.html', {'page_obj': page_obj, "form": form})
    except ObjectDoesNotExist as e:
        print("Error:", e)
        return redirect("create_profile_page")
    except Exception as e:
        print("Unhandled Error:", e)
        return JsonResponse({'error': str(e)}, status=500)







def delete_note(request, pk):
    if request.user.is_authenticated:
        note = get_object_or_404(Note, id=pk)
        #check if user owns note
        if request.user.profile == note.author_profile:
            note.delete()
            #messages
            print("Note Deleted")
            return redirect('home')
        else:
            #messages
            print("not your note")
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
                    print("error1")
            else:
                #messages
                print("error2")
                print("not your note")
                return render(request, 'homepage/edit_note.html', {'form':form, 'note':note})
        else:
            print("error3")
            success_url = reverse_lazy('home')