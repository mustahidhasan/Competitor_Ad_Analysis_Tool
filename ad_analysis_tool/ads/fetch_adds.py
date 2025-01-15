from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adsinsights import AdsInsights

# Step 1: Initialize the API
ACCESS_TOKEN = 'your_access_token'
APP_ID = 'your_app_id'
APP_SECRET = 'your_app_secret'

# Initialize the API with your credentials
FacebookAdsApi.init(access_token=ACCESS_TOKEN, app_id=APP_ID, app_secret=APP_SECRET)

# Step 2: Fetch Ad Account Details
print("Fetching Ad Accounts...")
me = User(fbid='me')
accounts = me.get_ad_accounts(fields=['id', 'name', 'account_status'])

if not accounts:
    print("No ad accounts found.")
    exit()

# Select the first Ad Account
ad_account = accounts[0]
AD_ACCOUNT_ID = ad_account['id']
print(f"Using Ad Account ID: {AD_ACCOUNT_ID}, Name: {ad_account['name']}")

# Step 3: Fetch Ads from the Ad Account
print("\nFetching Ads...")
ad_account_obj = AdAccount(AD_ACCOUNT_ID)
ads = ad_account_obj.get_ads(fields=[
    Ad.Field.id,
    Ad.Field.name,
    Ad.Field.status,
    Ad.Field.creative,
])

for ad in ads:
    print(f"Ad ID: {ad['id']}, Name: {ad['name']}, Status: {ad['status']}")

# Step 4: Fetch Ad Insights (Performance Metrics)
print("\nFetching Ad Insights...")
insights = ad_account_obj.get_insights(
    fields=[
        AdsInsights.Field.impressions,
        AdsInsights.Field.clicks,
        AdsInsights.Field.spend,
    ],
    params={
        'level': 'ad',           # Get insights at the ad level
        'date_preset': 'last_7d' # Data for the last 7 days
    }
)

for insight in insights:
    print(f"Ad ID: {insight.get('ad_id', 'N/A')}, Impressions: {insight.get('impressions', 0)}, Clicks: {insight.get('clicks', 0)}, Spend: ${insight.get('spend', 0)}")

# Step 5: Fetch Campaigns
print("\nFetching Campaigns...")
campaigns = ad_account_obj.get_campaigns(fields=[
    'id',
    'name',
    'status'
])

for campaign in campaigns:
    print(f"Campaign ID: {campaign['id']}, Name: {campaign['name']}, Status: {campaign['status']}")

# Step 6: Fetch Ad Sets
print("\nFetching Ad Sets...")
ad_sets = ad_account_obj.get_ad_sets(fields=[
    'id',
    'name',
    'status'
])

for ad_set in ad_sets:
    print(f"Ad Set ID: {ad_set['id']}, Name: {ad_set['name']}, Status: {ad_set['status']}")

print("\nProcess Complete!")
