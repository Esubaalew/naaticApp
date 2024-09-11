from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings

from shop import views


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('order/<int:product_id>/', views.order_product, name='order_product'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('order_success/', views.order_success, name='order_success'),
     path('edit-profile/', views.profile_view, name='edit_profile'),
 

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)