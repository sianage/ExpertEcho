from Homepage.models import Note
from django import forms


class NoteForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(attrs={
                               "placeholder":"Enter Note",
                               "class":"form-control"
                           }),
                           label="",)

    class Meta:
        model = Note
        exclude = ("profile","user")