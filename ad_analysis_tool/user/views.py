from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from .forms import SignUpForm


def home(request):
    return render(request, "user/home.html",)


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")


def register_user(request):
    # if request.method == "POST":
    #     form = SignUpForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         # authenticate and login
    #         username = form.cleaned_data["username"]
    #         password = form.cleaned_data["password1"]
    #         user = authenticate(username=username, password=password)
    #         login(request, user)
    #         messages.success(request, "You have successfully Registered")
    #         return redirect("home")
    # else:
    #     form = SignUpForm()
    #     return render(request, "register.html", {"form": form})
    return render(request, "user/register.html")