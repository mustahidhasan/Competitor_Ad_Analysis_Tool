import json
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from dotenv import load_dotenv
import os

load_dotenv()

class MessangerAd:

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

    def get_ads_messanger(self):
        # Get the Ad Account (use the first account)
        ad_account = AdAccount(self.accounts[0]['id'])

        # Fetch Ads and check the structure of the returned fields
        ads = ad_account.get_ads(fields=[
            Ad.Field.id,
            Ad.Field.name,
            Ad.Field.status,
            Ad.Field.effective_status,
            Ad.Field.created_time,
            Ad.Field.updated_time,
            Ad.Field.adset_id,
            Ad.Field.creative,
            AdSet.Field.targeting,
        ])
        # Check the structure of each ad and filter Messenger Ads
        messenger_ads = []
        for ad in ads:
            targeting=ad.get('targeting')
            # Ensure adset_id is string for comparison
            publisher_platforms = targeting.get("publisher_platforms", [])
    
            # Check if 'messenger' is in the publisher_platforms list
            if 'messenger' in publisher_platforms:
                messenger_ads.append(ad)

        # Create a list to store the structured JSON data
        messenger_ads_data = []

        # Get the creative (image/video) details for Messenger Ads
        for ad in messenger_ads:
            creative_id = ad['creative']['id']  # Get the creative ID from the ad
            creative = AdCreative(creative_id).api_get(fields=[
                AdCreative.Field.id,
                AdCreative.Field.name,
                AdCreative.Field.thumbnail_url,  # Thumbnail image URL (if exists)
                AdCreative.Field.image_url,       # Image URL (if exists)
                AdCreative.Field.video_id,        # Video ID (if exists)
            ])

            # Create the JSON structure for this ad
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

            # Append to the list of ads data
            messenger_ads_data.append(ad_data)

        # Print the structured data as JSON
        print("\n--- Messenger Ads Data (JSON Format) ---")
        messanger_output = json.dumps(messenger_ads_data, indent=4)
        return messanger_output

