from django.shortcuts import render

# Create your views here.

from .models import User

def home(request):
    if request.user.is_authenticated():
        username_is = "Moritz is using context"
        context = {"username_is": request.user}
    else:
        context = {"username_is": request.user}


    template = 'zettels/home.html'
    return render(request, template, context)


def all(request):
    allezettels = User.objects.all()
    context = {'zettels': allezettels}
    template = 'zettels/all.html'   
    return render(request, template, context)
