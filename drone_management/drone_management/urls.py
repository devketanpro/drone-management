"""
URL configuration for drone_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from drones_api.views import (BatteryStatus, RegisterDrone,
    UnAvailableDrone, AvailableDrone, LoadMedication, DroneLoadView,
    BatteryHistory
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('battery_status/<int:id>/', BatteryStatus.as_view(), name='battery_status'),
    path('register_drone/', RegisterDrone.as_view(), name='register_drone'),
    path('drones/<int:id>/load_medication/', LoadMedication.as_view(), name='load_medication'),
    path('drones/<int:id>/drone_load/', DroneLoadView.as_view(), name='drone_load'),
    path('unavailable_drones/', UnAvailableDrone.as_view(), name='unavailable_drones'),
    path('available_drones/', AvailableDrone.as_view(), name='available_drones'),
    path('battery_history/', BatteryHistory.as_view(), name='battery_history'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)