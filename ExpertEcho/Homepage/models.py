from ckeditor.fields import RichTextField
from django.db import models

from Members.models import Profile, CustomUser


class Note(models.Model):
    user = models.ForeignKey(CustomUser, related_name="Notes", on_delete=models.DO_NOTHING)
    body = RichTextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    author_profile = models.ForeignKey(Profile, related_name="Notes", on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return(f"{self.user} \n"
               f" {self.body}\n"
               f"(Note made {self.created:%Y-%m-%d %H:%M})")

