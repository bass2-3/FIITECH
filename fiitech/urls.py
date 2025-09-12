from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Personnalisation du titre de l'admin
admin.site.site_header = "FiiTech Solutions - Administration"
admin.site.site_title = "FiiTech Admin"
admin.site.index_title = "Panneau d'administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('content.urls')),
]

# Servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)