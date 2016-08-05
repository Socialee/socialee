from django.shortcuts import render, redirect

from .forms import PasswordForm


def simple_password(request):
    """
    Checks a password
    """
    if request.method == "POST":
        form = PasswordForm(data=request.POST)
        if form.is_valid():
            # TODO: set session with better param
            request.session["simple_auth"] = True
            return redirect(form.cleaned_data["url"] or "/")
    else:
        form = PasswordForm()
    return render(request, "simple_auth/password_form.html",
                  {"form": form})
