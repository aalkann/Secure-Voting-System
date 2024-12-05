from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('voting_app.urls')),
    path('authentication/', include('authentication_app.urls')),
    path("admin/", admin.site.urls),
]