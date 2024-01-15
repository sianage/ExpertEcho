from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from ExpertEcho.Debates.forms import CommentForm
from ExpertEcho.Debates.models import Debate
#import self as self
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from ExpertEcho.Blogs.forms import PostForm
from ExpertEcho.Debates.forms import DebateForm
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
from ExpertEcho.Blogs.models import Post, Category
from ExpertEcho.Members.models import CustomUser
from ExpertEcho.Homepage.models import Note
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from ExpertEcho.Homepage.forms import NoteForm
from ExpertEcho.Debates.forms import CommentForm

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
    return render(request, 'MainApp/debate/comment.html',
                  {'post': post, 'form': form, 'comment': comment})


class user_debate_list(ListView):
    print("DEBATE LIST")
    model = Debate
    template_name = 'MainApp/debate/user_debates.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Debate.objects.filter(author_id=author_id)
        else:
            return Debate.objects.all()


class debate_list(ListView):
    print("DEBATE LIST")
    model = Debate
    template_name = 'MainApp/debate/debate_list.html'

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
    template_name = 'MainApp/debate/economics_debate_list.html'

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
    template_name = 'MainApp/debate/polisci_debate_list.html'

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
    template_name = 'MainApp/debate/medicine_debate_list.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Debate.objects.filter(author_id=author_id)
        else:
            return Debate.objects.all()


class debate_detail(DetailView):
    model = Debate
    template_name = 'MainApp/debate/debate_detail.html'

class AddDebateView(LoginRequiredMixin, CreateView):
    model = Debate
    form_class = DebateForm
    template_name = 'MainApp/debate/add_debate.html'
    success_url = reverse_lazy('MainApp:debate_list')


def AddCommentView(request, pk):
    debate = get_object_or_404(Debate, id=pk)
    comment = get_object_or_404(Debate, id=pk)
    user = request.user
    opponent = debate.opponent
    comments = debate.comments.all()

    # Initialize form
    form = CommentForm(request.POST or None)

    # Check if the user is the author or opponent
    if user != debate.author and user != opponent:
        return redirect('MainApp:home')

    last_comment = comments.last()
    last_commenter_name = last_comment.commenter_name
    if last_commenter_name == request.user:
        return redirect('MainApp:home')
    else:
        form = CommentForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            comment = form.save(commit=False)
            comment.debate_id = pk
            comment.save()
            return redirect('MainApp:home')

    return render(request, 'MainApp/debate/add_comment.html', {'form': form, 'debate': debate})
