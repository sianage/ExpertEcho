from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from Debates.forms import CommentForm
from Debates.models import Debate
#import self as self
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from Blogs.forms import PostForm
from Debates.forms import DebateForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, request
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, CreateView
from .models import Debate, Comment
from Blogs.models import Post
from Members.models import CustomUser, Profile
from Homepage.models import Note
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from Homepage.forms import NoteForm
from Debates.forms import CommentForm

@require_POST
def debate_post(request, debate_id):
    print("DEBATE POST")
    post = get_object_or_404(Debate, id=debate_id)
    comment = None
    # ???????????????????????????????
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'debate/comment.html',
                  {'post': post, 'form': form, 'comment': comment})


class user_debate_list(ListView):
    print("DEBATE LIST")
    model = Debate
    template_name = 'debates/user_debates.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("debate author_id =", author_id)
        try:
            if author_id:
                author_profile = get_object_or_404(Profile, id=author_id)
                return Debate.objects.filter(author_profile=author_profile)
            else:
                return Debate.objects.all()
        except Http404:
            return Debate.objects.none()


class debate_list(ListView):
    print("DEBATE LIST")
    model = Debate
    template_name = 'debate/debate_list.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Debate.objects.filter(author_id=author_id)
        else:
            return Debate.objects.all()


class economics_debate_list(ListView):
    print("ECON DEBATE LIST")
    model = Debate
    template_name = 'debate/economics_debate_list.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Debate.objects.filter(author_id=author_id)
        else:
            return Debate.objects.all()


class polisci_debate_list(ListView):
    print("POLISCI DEBATE LIST")
    model = Debate
    template_name = 'debate/polisci_debate_list.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Debate.objects.filter(author_id=author_id)
        else:
            return Debate.objects.all()


class medicine_debate_list(ListView):
    print("MEDICINE DEBATE LIST")
    model = Debate
    template_name = 'debate/medicine_debate_list.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Debate.objects.filter(author_id=author_id)
        else:
            return Debate.objects.all()


class debate_detail(DetailView):
    model = Debate
    template_name = 'debates/debate_detail.html'

'''class AddDebateView(LoginRequiredMixin, CreateView):
    model = Debate
    form_class = DebateForm
    template_name = 'debate/start_debate.html'
    success_url = reverse_lazy('debate_list')'''


from django.shortcuts import get_object_or_404

# views.py
from django.shortcuts import render, get_object_or_404
from .forms import DebateForm
from .models import Debate


def create_debate(request):
    # Fetch opponents with the same academic field as the author_profile
    opponents = Profile.objects.filter(academic_field=request.user.profile.academic_field).exclude(user=request.user)

    if opponents.exists():
        opponent_list = [(profile.user.id, f'{profile.first_name} {profile.last_name}') for profile in opponents]
        print("opponent list 1:", opponent_list)
    else:
        opponent_list = []
        print("opponent list 2:", opponent_list)

    form = DebateForm(opponent_choices=opponent_list)

    if request.method == 'POST':
        form = DebateForm(request.POST)
        form.set_opponent_choices(opponent_list)
        print("opponent list 3",opponent_list)
        if form.is_valid():
            # Set the author_profile to the currently signed-in user's profile
            form.instance.author_profile = request.user.profile
            print("opponent list 4:", opponent_list)
            # Process the form data, save the Debate instance, etc.
            form.save()

    return render(request, 'debates/start_debate.html', {'form': form})


def AddCommentView(request, pk):
    debate = get_object_or_404(Debate, id=pk)
    user = request.user
    opponent = debate.opponent
    comments = debate.comments.all()

    # Check if the user is the author or opponent
    if user != debate.author_profile.user and user != opponent:
        return redirect('comment')

    # Determine the current commenter
    last_comment = comments.last()
    last_commenter_profile = last_comment.commenter_name if last_comment else None

    if last_commenter_profile == user.profile:
        current_commenter = opponent
    else:
        current_commenter = debate.author_profile.user

    # Initialize form
    form = CommentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.debate_id = pk
        comment.commenter_name = current_commenter.profile
        comment.save()

        return redirect('home')

    return render(request, 'debates/add_comment.html', {'form': form, 'debate': debate})
