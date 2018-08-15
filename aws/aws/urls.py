"""aws URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from lib import views as lib_views

admin.autodiscover()

urlpatterns = [
    # path('', views_accounts.app_login, name='login'),
    path('', lib_views.dashboard, name='dashboard'),
    path('iam/', include('iam.urls')),
    path('ec2/', include('ec2.urls')),
    # path('lib/', include('lib.urls')),
    path('admin/', admin.site.urls),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
