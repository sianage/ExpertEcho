from django.db import models

class Note(models.Model):
    user = models.ForeignKey(User, related_name="Notes", on_delete=models.DO_NOTHING)
    body = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, related_name="Notes", on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return(f"{self.user} \n"
               f" {self.body}\n"
               f"(Note made {self.created_at:%Y-%m-%d %H:%M})")