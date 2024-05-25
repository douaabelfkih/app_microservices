
from django.contrib import admin
from django.urls import path, include
from products.views import productView,ProductPageView,ProductDetailsView,verifier_authentification, add_to_cart, ProductListView, index, view_product,view_product1
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'products', productView, 'product')

urlpatterns = [
    path('api/', include(router.urls)),
    path('product-details-page/<str:slug>/', ProductDetailsView.as_view(), name='product_details_api'),
    path('products/', ProductListView.as_view(), name='products'),
    path('add-to-cart/<int:prodid>/', add_to_cart, name='check_authentication_and_add_to_cart'),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('item/<str:slug>/', view_product, name='view_product'),
    path('prd/<int:id>/', view_product1, name='view_product1'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
