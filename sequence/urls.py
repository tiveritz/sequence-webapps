from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('project.urls')),
    path('cms/', include('cms.urls')),
    path('webapp/admin/', admin.site.urls),
]
