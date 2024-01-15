from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .forms import ChoiceFormSet, PollForm, ChoiceForm
from .models import Poll, Choice, Vote
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required


class philosophy_poll_list(ListView):
    model = Poll
    template_name = 'poll/philosophy_poll_list.html'
    # return render(request, 'poll/philosophy_poll_list.html')


class economics_poll_list(ListView):
    model = Poll
    template_name = 'poll/economics_poll_list.html'
    # return render(request, 'poll/philosophy_poll_list.html')


class polisci_poll_list(ListView):
    model = Poll
    template_name = 'poll/polisci_poll_list.html'
    # return render(request, 'poll/philosophy_poll_list.html')


class medicine_poll_list(ListView):
    model = Poll
    template_name = 'poll/medicine_poll_list.html'
    # return render(request, 'poll/philosophy_poll_list.html')


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    user = request.user
    if Vote.objects.filter(user=user, choice__poll=poll).exists():
        return HttpResponseRedirect(reverse('results', args=(poll.id,)))
    else:
        return render(request, 'poll/poll_detail.html', {'poll': poll})


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

    return render(request, 'poll/results.html', {'poll': poll, 'choices': choices, 'total_votes': total_votes})

def CreatePollView(request):
    ChoiceFormSet = formset_factory(ChoiceForm, extra=1)

    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST, prefix='choices')

        if poll_form.is_valid() and choice_formset.is_valid():
            poll = poll_form.save(commit=False)
            poll.save()

            for choice_form in choice_formset:
                choice = choice_form.save(commit=False)
                choice.poll = poll
                choice.save()

            return redirect('MainApp:home')  # Redirect to the desired page after successful submission
    else:
        poll_form = PollForm()
        choice_formset = ChoiceFormSet(prefix='choices')

    return render(request, 'poll/create_poll.html', {
        'poll_form': poll_form,
        'choice_formset': choice_formset,
    })


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    user = request.user

    if poll.category.category.lower() != user.profile.academic_field.lower():
        return HttpResponseRedirect(reverse('results', args=(poll.id,)))

    if Vote.objects.filter(user=user, choice__poll=poll).exists():
        return render(request, 'poll/poll_detail.html', {'poll': poll, 'error_message': "You have already voted."})

    try:
        selected_choice_id = request.POST.get('choice')
        if selected_choice_id is None:
            raise KeyError
        selected_choice = poll.choice_set.get(pk=selected_choice_id)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'poll/poll_detail.html', {'poll': poll, 'error_message': "Invalid choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        Vote.objects.create(user=user, choice=selected_choice)
        return HttpResponseRedirect(reverse('results', args=(poll.id,)))


from django.shortcuts import render

# Create your views here.
