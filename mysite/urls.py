from django.contrib import admin
from django.urls import path, include
from main import views 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'brands', views.BrandViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
  
    path('api/v1/', include(router.urls)),
    path('api/v2/reviews/', views.ReviewAPIView.as_view()),
    path('api/v2/messages/', views.ContactMessageAPIView.as_view()),

   
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    
   
    path('profile/', views.profile, name='profile'),

   
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

   
    path('external-gadgets/', views.external_gadgets, name='external_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)