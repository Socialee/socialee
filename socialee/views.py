import os

from django.conf import settings
from django.views.generic import TemplateView
from .forms import SignupForm
from allauth.account.views import SignupView, RedirectAuthenticatedUserMixin

# Overwrite/disable dispatch method of RedirectAuthenticatedUserMixin (endless redirect on /).
def dispatch_no_redirect(self, request, *args, **kwargs):
    return super(RedirectAuthenticatedUserMixin, self).dispatch(request, *args, **kwargs)
RedirectAuthenticatedUserMixin.dispatch = dispatch_no_redirect


class Home(SignupView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['zettel_links'] = self.get_zettel_images("links")
        context['zettel_rechts'] = self.get_zettel_images("rechts")
        return context

    @classmethod
    def get_zettel_images(cls, subdir):
        subdir = os.path.join("zettels", subdir)
        filenames = list(os.walk(os.path.join(settings.MEDIA_ROOT, subdir)))
        try:
            l = [os.path.join(settings.MEDIA_URL, subdir, x)
                 for x in filenames[0][2] if x.endswith(".jpg")]
        except IndexError:
            return []
        return sorted(l)


class Cafe(TemplateView):
    template_name = 'cafe.html'

class Impressum(TemplateView):
    template_name = 'impressum.html'



    # project.object.get