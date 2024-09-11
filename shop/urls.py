from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from shop import views

import logging

logger = logging.getLogger(__name__)
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('order/<int:product_id>/', views.order_product, name='order_product'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


logger.debug(f"MEDIA_URL: {settings.MEDIA_URL}")
logger.debug(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")