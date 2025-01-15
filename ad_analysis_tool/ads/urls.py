from django.urls import path
from . import views

urlpatterns = [
    path('', views.configure, name='configure'),  # Configure page
    path('save_configuration', views.save_configuration, name='save_configuration'),  # Save configuration
    path('delete_configuration/<int:config_id>/', views.delete_configuration, name='delete_configuration'),  # Delete configuration
]
