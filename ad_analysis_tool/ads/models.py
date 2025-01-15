from django.db import models

# Create your models here.
class Configure(models.Model):
    configure_name = models.CharField(max_length=50, null=True, unique=True)
    ACCESS_TOKEN = models.TextField(null=True)
    APP_ID = models.CharField(max_length=200, null=True)
    APP_SECRET = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.configure_name} - {self.APP_ID}'

class SaveRawAdsData(models.Model):
    platform_name = models.CharField(max_length=100, null=True)
    raw_data = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.platform_name