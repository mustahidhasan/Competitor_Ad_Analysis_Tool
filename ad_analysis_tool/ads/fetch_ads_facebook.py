import json
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adset import AdSet
import os


class FacebookAd:

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

    def get_ads_facebook(self):
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
            AdSet.Field.targeting,
        ])

        all_ads = []  # List to store all ads and media information

        if not ads:
            print("No ads found for this account.")
        else:
            for ad in ads:
                ad_data = {
                    "Ad ID": ad.get('id', 'N/A'),
                    "Ad Name": ad.get('name', 'Unnamed Ad'),
                    "Status": ad.get('status', 'N/A'),
                    "Effective Status": ad.get('effective_status', 'N/A'),
                    "Ad Set ID": ad.get('adset_id', 'N/A'),
                    "Campaign ID": ad.get('campaign_id', 'N/A'),
                    "Creative ID": ad.get('creative', {}).get('creative_id', 'No Creative Found'),
                    "Created Time": ad.get('created_time', 'N/A'),
                    "Updated Time": ad.get('updated_time', 'N/A'),
                    "Creative Media": [],
                }

                # Fetch the Creative Media (Image/Video)
                creative_id = ad['creative']['id'] if 'creative' in ad else None
                if creative_id:
                    creative = AdCreative(creative_id).api_get(fields=[
                        AdCreative.Field.id,
                        AdCreative.Field.name,
                        AdCreative.Field.image_url,    # Image URL for ad
                        AdCreative.Field.video_id,     # Video ID for ad
                        AdCreative.Field.thumbnail_url,  # Thumbnail URL for video
                    ])
                    ad_data["Creative Media"].append({
                        "Creative Name": creative['name'],
                        "Image URL": creative.get('image_url', 'No Image URL'),
                        "Video ID": creative.get('video_id', 'No Video ID'),
                        "Thumbnail URL": creative.get('thumbnail_url', 'No Thumbnail URL')
                    })

                # Append the ad_data to the all_ads list
                all_ads.append(ad_data)

        # Convert the all_ads list to JSON format
        json_output = json.dumps(all_ads, indent=4)
        # print(json_output)
        return json_output


