from django.shortcuts import render

from .models import User

def all(request):
    allezettels = User.objects.all()
    context = {'zettels': allezettels}
    template = 'zettels/all.html'   
    return render(request, template, context)
