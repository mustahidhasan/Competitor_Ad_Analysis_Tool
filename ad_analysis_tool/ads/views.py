from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Configure

def configure(request):
    # Fetch all configurations to display in the table
    configurations = Configure.objects.all()
    return render(request, 'configure.html', {'configurations': configurations})


def save_configuration(request):
    # Handle saving a new configuration
    if request.method == "POST":
        configure_name = request.POST.get('configure_name')
        access_token = request.POST.get('access_token')
        app_id = request.POST.get('app_id')
        app_secret = request.POST.get('app_secrect')

        # Validate unique configuration name
        if Configure.objects.filter(configure_name=configure_name).exists():
            messages.error(request, "Configuration name must be unique.")
        else:
            Configure.objects.create(
                configure_name=configure_name,
                ACCESS_TOKEN=access_token,
                APP_ID=app_id,
                APP_SECRET=app_secret
            )
            messages.success(request, "Configuration saved successfully.")

    return redirect('configure')  # Redirect back to the configure page


def delete_configuration(request, config_id):
    # Delete the configuration by ID
    config = get_object_or_404(Configure, id=config_id)
    config.delete()
    messages.success(request, "Configuration deleted successfully.")
    return redirect('configure')  # Redirect back to the configure page
