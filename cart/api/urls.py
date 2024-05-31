from django.urls import path
from .views import *

urlpatterns = [
    path('test/', test, name='test'),
    path('cart/<int:user_id>/', CartView.as_view(), name='cart'),
    path('cart/<int:product_id>/<int:user_id>/', CartView.as_view(), name='cart_modify'),
    #path('cart/remove/<int:product_id>/', CartView.as_view(), name='remove_from_cart'),

]
