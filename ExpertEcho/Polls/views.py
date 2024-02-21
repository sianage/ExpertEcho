from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .forms import ChoiceFormSet, PollForm, ChoiceForm
from .models import Poll, Choice, Vote
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

def economics_polls(request):
    polls = Poll.objects.all()
    return render(request, 'polls/economics_polls.html', {'polls': polls})

def finance_polls(request):
    polls = Poll.objects.all()
    return render(request, 'polls/finance_polls.html', {'polls': polls})

def law_polls(request):
    polls = Poll.objects.all()
    return render(request, 'polls/law_polls', {'polls': polls})

def medicine_polls(request):
    polls = Poll.objects.all()
    return render(request, 'polls/medicine_polls.html', {'polls': polls})

def tech_polls(request):
    polls = Poll.objects.all()
    return render(request, 'polls/tech_polls.html', {'polls': polls})


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    user = request.user
    if Vote.objects.filter(user=user, choice__poll=poll).exists():
        return HttpResponseRedirect(reverse('results', args=(poll.id,)))
    else:
        return render(request, 'polls/poll_detail.html', {'poll': poll})


def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choices = poll.choice_set.all()
    total_votes = sum(choice.votes for choice in choices)

    # Calculate the percentage for each choice
    for choice in choices:
        if total_votes > 0:
            choice.percentage = (choice.votes / total_votes) * 100
        else:
            choice.percentage = 0

    return render(request, 'polls/results.html', {'poll': poll, 'choices': choices, 'total_votes': total_votes})


@login_required
def CreatePollView(request):
    ChoiceFormSet = formset_factory(ChoiceForm, extra=1)

    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST, prefix='choices')

        if poll_form.is_valid() and choice_formset.is_valid():
            # Save the poll first
            poll = poll_form.save(commit=False)
            poll.author_profile = request.user.profile
            poll.category = poll.author_profile.academic_field.capitalize()
            poll.save()

            for choice_form in choice_formset:
                choice = choice_form.save(commit=False)
                choice.poll = poll  # Set the poll instance for the choice
                choice.save()

            return redirect('vote', poll_id=poll.id)


    else:
        poll_form = PollForm()
        choice_formset = ChoiceFormSet(prefix='choices')

    return render(request, 'polls/create_poll.html', {
        'poll_form': poll_form,
        'choice_formset': choice_formset,
    })

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    user = request.user

    if poll.category.lower() != user.profile.academic_field.lower():
        return HttpResponseRedirect(reverse('results', args=(poll.id,)))

    if Vote.objects.filter(user=user, choice__poll=poll).exists():
        return render(request, 'polls/poll_detail.html', {'poll': poll, 'error_message': "You have already voted."})

    try:
        selected_choice_id = request.POST.get('choice')
        if selected_choice_id is None:
            raise KeyError
        selected_choice = poll.choice_set.get(pk=selected_choice_id)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/poll_detail.html', {'poll': poll, 'error_message': "Invalid choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        Vote.objects.create(user=user, choice=selected_choice)
        return HttpResponseRedirect(reverse('results', args=(poll.id,)))


from django.shortcuts import render

# Create your views here.
