from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import FormView
from allauth.account.views import SignupView

from .forms import *
from .models import Idea


class CreateIdea(SignupView):
    model = Idea
    template_name = 'create_idea.html'
    form_class = IdeaForm
    success_url = reverse_lazy('idea_list')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            pic = request.FILES['picture']
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            ret = super(CreateIdea, self).post(request, *args, **kwargs)
            if pic or title or description:
                newPic = Idea.objects.create( picture = pic, title = title, description = description )
                newPic.save()
            return ret
        else:
            return self.form_invalid(form)


def idea_list(request):
    idea_list = Idea.objects.filter(active=True).order_by('-subm_date')
    context = {
        "idea_list": idea_list,
    }
    
    return render(request, "idea_list.html", context)


class Like(UpdateView):
    template_name = 'like_counts.html'

    def post(self, request, *args, **kwargs):
        idea_id = request.POST.get('idea_id')

        instance = Idea.objects.get(id=idea_id)
        if self.request.user in instance.likes.all():
            instance.likes.remove(self.request.user)
        else:
            instance.likes.add(self.request.user)

        return render(request, self.template_name, {'idea' : instance} )
