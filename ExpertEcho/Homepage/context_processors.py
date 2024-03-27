from Blogs.models import Post
from Members.models import Profile
from Debates.models import Debate
from .forms import NoteForm

def sidebar_content(request):
    if not request.user.is_authenticated:
        return {}

    try:
        profile = request.user.profile
        followed_profiles = profile.follows.all()

        sidebar_blogs = Post.published.exclude(author_profile__in=followed_profiles).order_by("-publish")[:5]
        sidebar_debates = Debate.objects.exclude(author_profile__in=followed_profiles).order_by("-created")[:5]

        return {
            'sidebar_blogs': sidebar_blogs,
            'sidebar_debates': sidebar_debates,
        }
    except Profile.DoesNotExist:
        return {}


def note_form(request):
    return {'form': NoteForm()}
