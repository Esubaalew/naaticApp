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
urlpatterns += [
    path('mini-app/', views.mini_app_view, name='mini_app'),
]
urlpatterns += [
    path('api/products/', views.api_product_list, name='api_product_list'),
    path('api/order/', views.api_order_create, name='api_order_create'),
    path('api/login/', views.api_login, name='api_login'),
     path('api/check-auth/', views.check_auth, name='check_auth'),
      path('api/signup/', views.api_signup, name='api_signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)