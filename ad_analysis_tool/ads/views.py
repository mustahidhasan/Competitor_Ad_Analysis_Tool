from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Configure
from .fetch_ads_facebook import FacebookAd  # Import the FacebookAd class
from .fetch_ads_messanger import MessangerAd
from .fetch_ads_insta import InstagramAd
def generate_ads(request):
    if request.method == "POST":
        # Get the selected configuration ID from the form
        config_id = request.POST.get("configuration")
        platform = request.POST.get("platforms")
        
        if config_id:
            # Fetch the selected configuration from the database
            config = get_object_or_404(Configure, id=config_id)

            # Extract the credentials (ACCESS_TOKEN, APP_ID, APP_SECRET) from the selected configuration
            ACCESS_TOKEN = config.ACCESS_TOKEN  # Ensure you have these fields in your Configure model
            APP_ID = config.APP_ID
            APP_SECRET = config.APP_SECRET

            try:
                if platform == "facebook":
                    # Create an instance of the FacebookAd class with the retrieved credentials
                    facebook_ad = FacebookAd(ACCESS_TOKEN, APP_ID, APP_SECRET)
                    # Call the method to fetch ads from Facebook
                    facebook_ad_data = facebook_ad.get_ads_facebook()
                    print("line 26", facebook_ad_data)

                    # You can also render some success message or data to the template if needed
                    messages.success(request, "Facebook Ads fetched successfully!")
                    return redirect("home")  # Redirect to home after successful fetch
                
                elif platform == "messenger":
                    # Create an instance of the messanger class with the retrieved credentials
                    messanger_ad = MessangerAd(ACCESS_TOKEN, APP_ID, APP_SECRET)
                    # Call the method to fetch ads from Facebook
                    messanger_ad_data = messanger_ad.get_ads_messanger()
                    print("line 39", messanger_ad_data)

                    # You can also render some success message or data to the template if needed
                    messages.success(request, "Messanger Ads fetched successfully!")
                    return redirect("home")  # Redirect to home after successful fetch
                
                elif platform == "instagram":
                    # Create an instance of the insta class with the retrieved credentials
                    insta_ad = InstagramAd(ACCESS_TOKEN, APP_ID, APP_SECRET)
                    # Call the method to fetch ads from Facebook
                    insta_ad_data = insta_ad.get_ads_instagram()
                    print("line 50", insta_ad_data)

                    # You can also render some success message or data to the template if needed
                    messages.success(request, "Insta Ads fetched successfully!")
                    return redirect("home")  # Redirect to home after successful fetch

                else:
                    messages.error(request, "Ads did not fetched!")
                    return redirect("home")  # Redirect to home after successful fetch
            except Exception as e:
                messages.error(request, f"Error fetching ads: {e}")
                return redirect("home")

    else:
        # If GET request, render the page with available configurations
        configurations = Configure.objects.all()  # Get all configurations available
        return render(request, "home.html", {"configurations": configurations})


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
