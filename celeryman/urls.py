"""celeryman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from chassis.urls import urlpatterns as chassis_urls

from celeryman import views

# chassis_urls includes:
#  diagnostics/error
#  health/(live|ready|status)
#  docs/api/
#  admin/
#  admin_tools/
#
# see https://github.com/oreillymedia/chassis/blob/develop/chassis/core/urls.py for current list

urlpatterns = [
    # add your service's URLs here
    path('', views.index, name='home')
] + chassis_urls
