from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from Homepage.forms import NoteForm
from Homepage.models import Note
from Members.models import Profile


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'homepage/homepage.html')

    form = NoteForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            note = form.save(commit=False)
            note.profile = request.user.profile
            note.user = request.user
            note.save()
            return redirect('home')

    try:
        profile = request.user.profile
        followed_profiles = profile.follows.all()
        notes = Note.objects.filter(profile__in=followed_profiles).order_by("-created_at")
    except Profile.DoesNotExist:
        return redirect("create_profile_page")

    return render(request, 'homepage/homepage.html', {'notes': notes, "form": form})


def delete_note(request, pk):
    if request.user.is_authenticated:
        note = get_object_or_404(Note, id=pk)
        #check if user owns note
        if request.user.profile == note.profile:
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
        if request.user.profile == note.profile:
            form = NoteForm(request.POST or None, instance=note)
            if request.method == "POST":
                if form.is_valid():
                    note = form.save(commit=False)
                    note.profile = request.user.profile
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