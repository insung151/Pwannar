from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('message/', include('message.urls', namespace='messages')),
    path('team/', include('team.urls', namespace='team')),
    path('board/planning/', include('PlanningBoard.urls', namespace='planningboard')),
    path('board/information/', include('InformationBoard.urls', namespace='informationboard')),
    path('board/club/', include('ClubBoard.urls', namespace='cluboard'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)