import json
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative


class FacebookAd:
    def __init__(self, access_token, app_id, app_secret):
        """
        Initialize the Facebook Ads API and fetch ad account details.
        """
        self.access_token = access_token
        self.app_id = app_id
        self.app_secret = app_secret

        # Initialize the Facebook Ads API
        FacebookAdsApi.init(
            access_token=self.access_token,
            app_id=self.app_id,
            app_secret=self.app_secret,
        )

        # Fetch ad accounts
        print("Fetching Ad Accounts...")
        user = User(fbid="me")
        self.accounts = user.get_ad_accounts(fields=["id", "name", "account_status"])

    def get_ads_facebook(self):
        """
        Fetch ads and creative data for the first ad account, returning as a list of dictionaries.
        """
        if not self.accounts:
            print("No ad accounts found.")
            return []

        # Use the first ad account
        ad_account = self.accounts[0]
        ad_account_id = ad_account["id"]
        print(f"Using Ad Account ID: {ad_account_id}, Name: {ad_account['name']}")

        # Fetch ads from the selected account
        print("\nFetching Ads with Detailed Information...")
        ad_account_obj = AdAccount(ad_account_id)
        ads = ad_account_obj.get_ads(
            fields=[
                Ad.Field.id,
                Ad.Field.name,
                Ad.Field.status,
                Ad.Field.effective_status,
                Ad.Field.adset_id,
                Ad.Field.campaign_id,
                Ad.Field.creative,
                Ad.Field.created_time,
                Ad.Field.updated_time,
            ]
        )

        if not ads:
            print("No ads found for this account.")
            return []

        all_ads = []
        for ad in ads:
            # Start building the ad data dictionary
            ad_data = {
                "ad_id": ad.get("id", "N/A"),
                "ad_name": ad.get("name", "Unnamed Ad"),
                "status": ad.get("status", "N/A"),
                "effective_status": ad.get("effective_status", "N/A"),
                "ad_set_id": ad.get("adset_id", "N/A"),
                "campaign_id": ad.get("campaign_id", "N/A"),
                "creative_id": ad.get("creative", {}).get("id", "No Creative Found"),
                "created_time": ad.get("created_time", "N/A"),
                "updated_time": ad.get("updated_time", "N/A"),
                "creative_name": "N/A",
                "image_url": "N/A",
                "video_id": "N/A",
                "thumbnail_url": "N/A",
            }

            # Fetch creative details if a creative ID is available
            creative_id = ad.get("creative", {}).get("id")
            if creative_id:
                try:
                    creative = AdCreative(creative_id).api_get(
                        fields=[
                            AdCreative.Field.id,
                            AdCreative.Field.name,
                            AdCreative.Field.image_url,
                            AdCreative.Field.video_id,
                            AdCreative.Field.thumbnail_url,
                        ]
                    )
                    # Merge creative data directly into the ad data
                    ad_data.update({
                        "creative_name": creative.get("name", "Unnamed Creative"),
                        "image_url": creative.get("image_url", "No Image URL"),
                        "video_id": creative.get("video_id", "No Video ID"),
                        "thumbnail_url": creative.get(
                            "thumbnail_url", "No Thumbnail URL"
                        ),
                    })
                except Exception as e:
                    print(f"Error fetching creative data for ID {creative_id}: {e}")
                    ad_data.update({
                        "creative_name": "Error fetching creative",
                        "image_url": "N/A",
                        "video_id": "N/A",
                        "thumbnail_url": "N/A",
                    })

            # Append the ad data to the result list
            all_ads.append(ad_data)

        return all_ads
