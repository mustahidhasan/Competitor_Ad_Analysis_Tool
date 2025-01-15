from django.contrib import admin
from .models import Configure, SaveRawAdsData

# Configure Model Admin Customization
class ConfigureAdmin(admin.ModelAdmin):
    list_display = ('configure_name', 'APP_ID', 'APP_SECRET')  # Display columns
    search_fields = ('configure_name', 'APP_ID')  # Enable search on configure_name and APP_ID fields
    list_filter = ('configure_name',)  # Add filtering option for configure_name
    
    # Optional: Add more customization like fieldsets or form widgets
    fieldsets = (
        (None, {
            'fields': ('configure_name', 'ACCESS_TOKEN', 'APP_ID', 'APP_SECRET')
        }),
    )

# Register Configure model with the customized admin
admin.site.register(Configure, ConfigureAdmin)

# SaveRawAdsData Model Admin Customization
class SaveRawAdsDataAdmin(admin.ModelAdmin):
    list_display = ('platform_name', 'created_at')  # Display platform name and timestamp
    search_fields = ('platform_name',)  # Enable search for platform_name
    list_filter = ('platform_name',)  # Allow filtering by platform_name
    readonly_fields = ('created_at',)  # Make created_at field read-only

# Register SaveRawAdsData model with the customized admin
admin.site.register(SaveRawAdsData, SaveRawAdsDataAdmin)
