from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from ads.models import Configure  # Assuming Configure model exists


def home(request):
    if request.method == "POST":
        if "username" in request.POST and "password" in request.POST:
            # Handle user login
            username = request.POST["username"]
            password = request.POST["password"]

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in")
                return redirect("home")
            else:
                messages.error(request, "There was an error logging in. Please try again.")
                return redirect("home")

        elif "configuration" in request.POST and "platforms" in request.POST:
            # Handle the selection of configuration and platforms for generating new ad
            selected_configuration = request.POST["configuration"]
            selected_platforms = request.POST.getlist("platforms")  # Multiple platforms can be selected
            
            # Process the selected configuration and platforms here (e.g., save or generate ads)
            messages.success(request, f"Ad generation selected for configuration: {selected_configuration} and platforms: {', '.join(selected_platforms)}")

            return redirect("home")
    
    if request.user.is_authenticated:
        # If the user is logged in, fetch configurations
        configurations = Configure.objects.all()
        context = {
            "configurations": configurations,
        }
        return render(request, "home.html", context)
    else:
        return render(request, "home.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # authenticate and login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully Registered")
            return redirect("home")
    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})
    return render(request, "register.html", {"form": form})
