import os
import urllib.request

from django.conf import settings
from django.views.generic import TemplateView

from allauth.account.views import RedirectAuthenticatedUserMixin, SignupView
import random
from .models import Project, Input, Output


# Overwrite/disable dispatch method of RedirectAuthenticatedUserMixin (endless redirect on /).
def dispatch_no_redirect(self, request, *args, **kwargs):
    return super(RedirectAuthenticatedUserMixin, self).dispatch(request, *args, **kwargs)
RedirectAuthenticatedUserMixin.dispatch = dispatch_no_redirect


class BaseView:
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        return context


class Home(BaseView, SignupView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['zettel_links'] = self.get_zettel_images("links")
        context['zettel_rechts'] = self.get_zettel_images("rechts")

        context['projects'] = list(Project.objects.all())
        for i in range(1, 311):
            context['projects'] += [Project(title='dummy' + str(i))]
        context['inputs'] = list(Input.objects.all())
        for i in range(1, 311):
            context['inputs'] += [Input(title='dummy' + str(i))]
        context['outputs'] = list(Output.objects.all())
        for i in range(1, 311):
            context['outputs'] += [Output(title='dummy' + str(i))]
        context['shuffled'] = context['outputs']+context['inputs']+context['projects']
        random.shuffle(context['shuffled'])
        print (context['shuffled'])
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

    # def home(request):
    #     projects = Project.objects.all()
    #     template = 'home.html'
    #     context = {"projects": projects}
    #     return render (request, template, context)


class Cafe(BaseView, TemplateView):
    template_name = 'cafe.html'

class Impressum(BaseView, TemplateView):
    template_name = 'impressum.html'

class Jumpage(BaseView, TemplateView):
    template_name = 'jumpage.html'

    def get_context_data(self, **kwargs):
        context = super(Jumpage, self).get_context_data(**kwargs)
        url = 'https://jumpage.com/1109292709086173'
        context['jumpage'] = urllib.request.urlopen(url).read()
        return context