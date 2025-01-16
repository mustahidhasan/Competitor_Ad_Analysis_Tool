from django.db import models


# Create your models here.
class Configure(models.Model):
    configure_name = models.CharField(max_length=50, null=True, unique=True)
    ACCESS_TOKEN = models.TextField(null=True)
    APP_ID = models.CharField(max_length=200, null=True)
    APP_SECRET = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.configure_name} - {self.APP_ID}"


class SaveRawAdsData(models.Model):
    platform_name = models.CharField(max_length=100, null=True)
    ad_id = models.CharField(max_length=255, null=False)  # Ensure ad_id is not nullable
    ad_name = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=50, null=True)
    effective_status = models.CharField(max_length=50, null=True)
    created_time = models.DateTimeField(null=True)
    updated_time = models.DateTimeField(null=True)
    creative_id = models.CharField(max_length=255, null=True)
    creative_name = models.CharField(max_length=255, null=True)
    image_url = models.URLField(null=True, blank=True)
    video_id = models.CharField(max_length=255, null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)
    raw_data = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("platform_name", "ad_id")  # Enforce uniqueness for platform and ad_id combination

    def __str__(self):
        return f"{self.platform_name} - {self.ad_id}"