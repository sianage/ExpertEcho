from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages  # Import this if not already done

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

from fields import FIELD_CHOICES
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
        opponent_id = self.request.GET.get('opponent') # to be used to access debates opponent is involved in
        print("debate author_id =", author_id)
        print("debate opponent_id =", opponent_id)
        try:
            if author_id:
                author_profile = get_object_or_404(Profile, id=author_id)
                return Debate.objects.filter(author_profile=author_profile)
            else:
                return Debate.objects.all()
        except Http404:
            return Debate.objects.none()


class debate_list(ListView):
    model = Debate
    template_name = 'debates/debate_list.html'

    def get_category_name(self, field_identifier):
        # Convert field identifier to human-readable name
        return dict(FIELD_CHOICES).get(field_identifier, "Unknown Category")

    def get_queryset(self):
        category = self.kwargs['category']
        queryset = Debate.objects.filter(category=category).select_related('author_profile', 'opponent')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_identifier = self.kwargs['category']
        context['category_name'] = self.get_category_name(category_identifier)
        return context


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

    # Prepare opponent choices for the form
    opponent_list = [(profile.id, f'{profile.first_name} {profile.last_name}') for profile in opponents]

    if request.method == 'POST':
        # Instantiate the form with POST data and opponent choices
        form = DebateForm(request.POST, opponent_choices=opponent_list)
        if form.is_valid():
            # Set the author_profile to the currently signed-in user's profile
            debate = form.save(commit=False)
            debate.author_profile = request.user.profile
            debate.save()
            # Redirect or further processing after saving the Debate instance
            return redirect('home')  # Replace 'some_view_name' with the name of the view to redirect to
    else:
        # Instantiate the form for a GET request with the opponent choices
        form = DebateForm(opponent_choices=opponent_list)

    return render(request, 'debates/start_debate.html', {'form': form})

from django.shortcuts import get_object_or_404

def AddCommentView(request, pk):
    debate = get_object_or_404(Debate, id=pk)
    user = request.user
    user_profile = user.profile  # Assuming 'user' has a 'profile' attribute
    opponent = debate.opponent

    # Check if the user is the author or opponent
    if user_profile != debate.author_profile and user_profile != opponent:
        messages.error(request, "You are not a participant in this debate.")
        return redirect('comment')

    comments = debate.comments.all()
    last_comment = comments.last()

    # Determine the current commenter and check if it's their turn
    if last_comment:
        last_commenter_profile = last_comment.commenter_name
        if last_commenter_profile == user_profile:
            messages.error(request, "You cannot comment twice in a row.")
            return redirect('home')  # Or some other appropriate redirect
    else:
        # If there are no comments, ensure the first commenter is the debate creator
        if user_profile != debate.author_profile:
            messages.error(request, "The debate creator must comment first.")
            return redirect('home')

    # Initialize form
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.debate = debate
        comment.commenter_name = user_profile  # user_profile is already a Profile instance
        comment.save()
        messages.success(request, "Your comment has been posted.")
        return redirect('home')

    return render(request, 'debates/add_comment.html', {'form': form, 'debate': debate})