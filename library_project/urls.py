from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('account/', include('accounts.urls')),
    path('new_material/', include('newmaterial.urls')),
    path('check_in_out/', include('check_in_out.urls')),
]
