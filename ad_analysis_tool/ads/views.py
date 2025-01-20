from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Configure, SaveRawAdsData
from .fetch_ads_facebook import FacebookAd  # Import the FacebookAd class
from .fetch_ads_messanger import MessangerAd
from .fetch_ads_insta import InstagramAd

from .analyse_ad import AdAnalyse
def generate_ads(request):
    if request.method == "POST":
        # Get the selected configuration ID and platform from the form
        config_id = request.POST.get("configuration")
        platform = request.POST.get("platforms")

        if config_id:
            # Fetch the selected configuration from the database
            config = get_object_or_404(Configure, id=config_id)

            # Extract credentials from the selected configuration
            ACCESS_TOKEN = config.ACCESS_TOKEN
            APP_ID = config.APP_ID
            APP_SECRET = config.APP_SECRET

            try:
                # Fetch ads data based on the selected platform
                if platform == "facebook":
                    facebook_ad = FacebookAd(ACCESS_TOKEN, APP_ID, APP_SECRET)
                    ads_data = facebook_ad.get_ads_facebook()

                elif platform == "messenger":
                    messanger_ad = MessangerAd(ACCESS_TOKEN, APP_ID, APP_SECRET)
                    ads_data = messanger_ad.get_ads_messanger()

                elif platform == "instagram":
                    insta_ad = InstagramAd(ACCESS_TOKEN, APP_ID, APP_SECRET)
                    ads_data = insta_ad.get_ads_instagram()

                else:
                    messages.error(request, "Invalid platform selected!")
                    return redirect("home")

                # Save each ad individually in the database, checking for redundancy
                for ad in ads_data:
                    ad_id = ad.get("ad_id")

                    if not ad_id:
                        print(f"Skipping ad due to missing 'ad_id': {ad}")
                        continue  # Skip this ad if 'ad_id' is missing

                    # Check for redundancy based on platform and ad_id (ensure ad_id is unique per platform)
                    if not SaveRawAdsData.objects.filter(platform_name=platform, ad_id=ad_id).exists():
                        creative = ad.get("creative", {})

                        # Handle cases where 'creative' data might be missing or incomplete
                        image_url = creative.get("image_url", ad.get("image_url", None))
                        video_id = creative.get("video_id", ad.get("video_id", None))
                        thumbnail_url = creative.get("thumbnail_url", ad.get("thumbnail_url", None))

                        SaveRawAdsData.objects.create(
                            platform_name=platform,
                            ad_id=ad["ad_id"],  # Ensure correct key for ad_id
                            ad_name=ad["ad_name"],
                            status=ad["status"],
                            effective_status=ad["effective_status"],
                            created_time=ad["created_time"],
                            updated_time=ad["updated_time"],
                            creative_id=creative.get("id", None),
                            creative_name=creative.get("name", None),
                            image_url=image_url,
                            video_id=video_id,
                            thumbnail_url=thumbnail_url,
                            raw_data=ad,  # Save the entire JSON data for reference
                        )
                        messages.success(request, f"{platform.capitalize()} Ads fetched successfully!")
                    else:
                        messages.error(request, f"Ad with ID {ad_id} already exists for platform {platform}. Skipping.")
                        print(f"Ad with ID {ad_id} already exists for platform {platform}. Skipping.")

                
                return redirect("home")

            except Exception as e:
                messages.error(request, f"Error fetching ads: {e}")
                return redirect("home")

    else:
        # If GET request, render the page with available configurations
        configurations = Configure.objects.all()
        return render(request, "home.html", {"configurations": configurations})



def configure(request):
    # Fetch all configurations to display in the table
    configurations = Configure.objects.all()
    return render(request, "configure.html", {"configurations": configurations})


def save_configuration(request):
    # Handle saving a new configuration
    if request.method == "POST":
        configure_name = request.POST.get("configure_name")
        access_token = request.POST.get("access_token")
        app_id = request.POST.get("app_id")
        app_secret = request.POST.get("app_secrect")

        # Validate unique configuration name
        if Configure.objects.filter(configure_name=configure_name).exists():
            messages.error(request, "Configuration name must be unique.")
        else:
            Configure.objects.create(
                configure_name=configure_name,
                ACCESS_TOKEN=access_token,
                APP_ID=app_id,
                APP_SECRET=app_secret,
            )
            messages.success(request, "Configuration saved successfully.")

    return redirect("configure")  # Redirect back to the configure page


def delete_configuration(request, config_id):
    # Delete the configuration by ID
    config = get_object_or_404(Configure, id=config_id)
    config.delete()
    messages.success(request, "Configuration deleted successfully.")
    return redirect("configure")  # Redirect back to the configure page

def data(request):
    if request.user.is_authenticated:
        # Fetch all ad data from the database
        ads = SaveRawAdsData.objects.all().order_by('-created_at')  # Or filter by platform or other criteria if needed
        return render(request, 'data.html', {'ads': ads})

    return render(request, 'data.html')

def analysis_data(request):
    data_all = []
    ads = SaveRawAdsData.objects.all().order_by('-created_at')
    for ad in ads:
        data_all.append(ad.raw_data)
    
    # Create an instance of the AdAnalyse class
    ad_analyse = AdAnalyse(data_all)

    # Process the data
    ad_analyse.process_data()

    # Perform the comparative analysis
    analysis_df = ad_analyse.comparative_analysis()

    # Convert DataFrame to a list of dictionaries to pass to the template
    analysis_data = analysis_df.to_dict(orient='records')

    # Return the data to the template
    return render(request, 'analysis_data.html', {"analysis_df": analysis_data})
