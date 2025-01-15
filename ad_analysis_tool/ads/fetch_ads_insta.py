import json
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adset import AdSet
from dotenv import load_dotenv
import os

load_dotenv()

class InstagramAd:

    def __init__(self, ACCESS_TOKEN,APP_ID,APP_SECRET):
        # Step 1: Initialize the API
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.APP_ID = APP_ID
        self.APP_SECRET = APP_SECRET

        FacebookAdsApi.init(access_token=self.ACCESS_TOKEN, app_id=self.APP_ID, app_secret=self.APP_SECRET)

        # Step 1: Fetch Ad Account Details
        print("Fetching Ad Accounts...")
        me = User(fbid='me')
        self.accounts = me.get_ad_accounts(fields=['id', 'name', 'account_status'])

    def get_ads_instagram(self):
        if not self.accounts:
            print("No ad accounts found.")
            exit()

        ad_account = self.accounts[0]
        AD_ACCOUNT_ID = ad_account['id']
        print(f"Using Ad Account ID: {AD_ACCOUNT_ID}, Name: {ad_account['name']}")

        # Step 2: Fetch Ads with Detailed Information
        print("\nFetching Ads with Detailed Information...")
        ad_account_obj = AdAccount(AD_ACCOUNT_ID)
        ads = ad_account_obj.get_ads(fields=[
            Ad.Field.id,
            Ad.Field.name,
            Ad.Field.status,
            Ad.Field.effective_status,
            Ad.Field.adset_id,
            Ad.Field.campaign_id,
            Ad.Field.creative,
            Ad.Field.created_time,
            Ad.Field.updated_time,
            AdSet.Field.targeting,  # Adding targeting to check for Instagram
        ])

        if not ads:
            print("No ads found for this account.")
        else:
            instagram_ads = []
            for ad in ads:
                targeting = ad.get('targeting', {})
                publisher_platforms = targeting.get("publisher_platforms", [])
                
                # Check if 'instagram' is in the publisher_platforms list
                if 'instagram' in publisher_platforms:
                    instagram_ads.append(ad)

            # Create a list to store the structured JSON data for Instagram Ads
            instagram_ads_data = []

            # Get the creative (image/video) details for Instagram Ads
            for ad in instagram_ads:
                creative_id = ad['creative']['id']  # Get the creative ID from the ad
                creative = AdCreative(creative_id).api_get(fields=[
                    AdCreative.Field.id,
                    AdCreative.Field.name,
                    AdCreative.Field.thumbnail_url,  # Thumbnail image URL (if exists)
                    AdCreative.Field.image_url,       # Image URL (if exists)
                    AdCreative.Field.video_id,        # Video ID (if exists)
                ])

                # Create the JSON structure for this Instagram ad
                ad_data = {
                    'ad_id': ad['id'],
                    'ad_name': ad['name'],
                    'status': ad['status'],
                    'effective_status': ad['effective_status'],
                    'created_time': ad['created_time'],
                    'updated_time': ad['updated_time'],
                    'creative_id': creative_id,
                    'creative_name': creative['name'],
                    'image_url': creative.get('image_url', None),
                    'video_id': creative.get('video_id', None),
                    'thumbnail_url': creative.get('thumbnail_url', None),
                }

                # Append to the list of Instagram ads data
                instagram_ads_data.append(ad_data)

            # Print the structured data as JSON for Instagram Ads
            print("\n--- Instagram Ads Data (JSON Format) ---")
            insta_output = json.dumps(instagram_ads_data, indent=4)
        return insta_output
        # print("\nProcess Complete!")
