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

    def __init__(self):
        # Initialize the API
        ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
        APP_ID = os.getenv("APP_ID")
        APP_SECRET = os.getenv("APP_SECRET")
        FacebookAdsApi.init(access_token=ACCESS_TOKEN, app_id=APP_ID, app_secret=APP_SECRET)

        # Step 1: Fetch Ad Account Details
        print("Fetching Ad Accounts...")
        me = User(fbid='me')
        self.accounts = me.get_ad_accounts(fields=['id', 'name', 'account_status'])

    def get_ad_instagram(self):
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
        ])

        if not ads:
            print("No ads found for this account.")
        else:
            for ad in ads:
                print("\n--- Ad Details ---")
                print(f"Ad ID: {ad.get('id', 'N/A')}")
                print(f"Ad Name: {ad.get('name', 'Unnamed Ad')}")
                print(f"Status: {ad.get('status', 'N/A')}")
                print(f"Effective Status: {ad.get('effective_status', 'N/A')}")
                print(f"Ad Set ID: {ad.get('adset_id', 'N/A')}")
                print(f"Campaign ID: {ad.get('campaign_id', 'N/A')}")
                print(f"Creative ID: {ad.get('creative', {}).get('creative_id', 'No Creative Found')}")
                print(f"Created Time: {ad.get('created_time', 'N/A')}")
                print(f"Updated Time: {ad.get('updated_time', 'N/A')}")

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
                    print(f"Creative Name: {creative['name']}")
                    if 'image_url' in creative:
                        print(f"Image URL: {creative['image_url']}")
                    if 'video_id' in creative:
                        print(f"Video ID: {creative['video_id']}")
                    if 'thumbnail_url' in creative:
                        print(f"Thumbnail URL: {creative['thumbnail_url']}")

        print("\nProcess Complete!")
        
if __name__ == "__main__":
    facebook_ad = InstagramAd()
    facebook_ad.get_ad_instagram()
