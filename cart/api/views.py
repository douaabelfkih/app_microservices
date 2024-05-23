from django.http import HttpResponse
import requests
from django.contrib.auth.models import User
from .models import CartItems, Cart
from .serializers import CartItemSerializer, CartSerializer

from django_redis import get_redis_connection
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView

import requests


def test(request):
    return HttpResponse('fine')

class CartView(APIView):
    def post(self, request, product_id):
        user_id = request.user.id
        cart_key = f"cart_{user_id}"
        redis_conn = get_redis_connection("default")
        redis_conn.hincrby(cart_key, product_id, 1)
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        user_id = request.user.id
        cart_key = f"cart_{user_id}"
        redis_conn = get_redis_connection("default")
        cart_items = redis_conn.hgetall(cart_key)
        cart = {int(k.decode('utf-8')): int(v.decode('utf-8')) for k, v in cart_items.items()}
        return Response(cart)

    def delete(self, request, product_id):
        user_id = request.user.id
        cart_key = f"cart_{user_id}"
        redis_conn = get_redis_connection("default")
        redis_conn.hdel(cart_key, product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    




""" def add_to_cart(request, product_id): 
    # Obtenir les détails de l'utilisateur à partir du microservice d'authentification
    #auth_service_url = 'http://20.199.21.250:8000/api/user-details/'  # Remplacer par l'URL réelle du microservice d'authentification
    #auth_response = requests.get(auth_service_url, headers={'Authorization': f'Bearer {request.auth}'})
    
   if auth_response.status_code == 200:
        user_details = auth_response.json()
        username = user_details['username']
        user, _ = User.objects.get_or_create(username=username)
    else:
        return HttpResponse("Unauthorized", status=401) """
"""     user = 'akremtest'
    # Obtenir les détails du produit à partir du microservice de produits
    products_service_url = f'http://20.199.21.250:8002/product-details-page/{product_id}/'  # Remplacer par l'URL réelle du microservice de produits
    products_response = requests.get(products_service_url)
    
    if products_response.status_code == 200:
        product_details = products_response.json()
        product_name = product_details['name']
        product_stock = product_details['stock']
        
        # Enregistrer l'élément dans le panier
        cart_item = CartItem.objects.create(user=user, product_id=product_id, quantity=1)
        
        return HttpResponse("Product added to cart successfully")
    else:
        return HttpResponse("Product not found", status=404) """

""" @api_view(['GET'])
#@permission_classes([IsAuthenticated])
def view_carts(request):
    # checking for the parameters from the URL
    if request.query_params:
        carts = Cart.objects.filter(**request.query_params.dict())
    else:
        carts = Cart.objects.all()

    # if there is something in items else raise error
    if carts:
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND) """

""" @api_view(['POST'])
def add_new_cart(request):
    cart = CartSerializer(data=request.data)
    if cart.is_valid():
        cart.save()
        return Response(cart.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_item_to_cart(request):
    cartitem = CartitemSerializer(data=request.data)
    if cartitem.is_valid():
        cartitem.save()
        return Response(cartitem.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        user = self.get_user()class CartView(APIView):
    def get(self, request):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        cart_items = redis_conn.hgetall(cart_key)
        cart = {int(k.decode('utf-8')): int(v.decode('utf-8')) for k, v in cart_items.items()}
        return Response(cart)

    def post(self, request, product_id):
        product_service_url = f"http://product-service/api/products/{product_id}/"
        product_response = requests.get(product_service_url)
        if product_response.status_code == 200:
            cart_key = f"cart_{request.user.id}"
            redis_conn = get_redis_connection("default")
            redis_conn.hincrby(cart_key, product_id, 1)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        redis_conn.hdel(cart_key, product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)user=user)
        else:
            session_id = self.request.session.session_key
            return self.queryset.filter(session_id=session_id)

    def get_user(self):    path('add/', add_to_cart, name='add_to_cart'),

    path('addcart/', add_new_cart, name='add_new_cart'),
    path('carts/', view_carts, name='view_carts'),
    path('additemtocart/', add_item_to_cart, name='add_item_to_cart'),

    path('api/cart/', CartView.as_view(), name='cart'),
    path('api/cart/items/', CartItemView.as_view(), name='cart-items'),
    path('api/cart/migrate/', MigrateCartView.as_view(), name='cart-migrate'),
        auth_header = self.request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            jwt_auth = JWTAuthentication()
            validated_token = jwt_authclass CartView(APIView):
    def get(self, request):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        cart_items = redis_conn.hgetall(cart_key)
        cart = {int(k.decode('utf-8')): int(v.decode('utf-8')) for k, v in cart_items.items()}
        return Response(cart)

    def post(self, request, product_id):
        product_service_url = f"http://product-service/api/products/{product_id}/"
        product_response = requests.get(product_service_url)
        if product_response.status_code == 200:
            cart_key = f"cart_{request.user.id}"
            redis_conn = get_redis_connection("default")
            redis_conn.hincrby(cart_key, product_id, 1)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        redis_conn.hdel(cart_key, product_id)
        return Response(status=status.class CartView(APIView):
    def get(self, request):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        cart_items = redis_conn.hgetall(cart_key)
        cart = {int(k.decode('utf-8')): int(v.decode('utf-8')) for k, v in cart_items.items()}
        return Response(cart)

    def post(self, request, product_id):
        product_service_url = f"http://product-service/api/products/{product_id}/"
        product_response = requests.get(product_service_url)
        if product_response.status_code == 200:
            cart_key = f"cart_{request.user.id}"
            redis_conn = get_redis_connection("default")
            redis_conn.hincrby(cart_key, product_id, 1)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        redis_conn.hdel(cart_key, product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)HTTP_204_NO_CONTENT).get_validated_token(token)
            return jwt_auth.get_user(validated_token)
        return None

class CartItemView(generics.CreateAPIVclass CartView(APIView):
    def get(self, request):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        cart_items = redis_conn.hgetall(cart_key)
        cart = {int(k.decode('utf-8')): int(v.decode('utf-8')) for k, v in cart_items.items()}
        return Response(cart)

    def post(self, request, product_id):
        product_service_url = f"http://product-service/api/products/{product_id}/"
        product_response = requests.get(product_service_url)
        if product_response.status_code == 200:
            cart_key = f"cart_{request.user.id}"
            redis_conn = get_redis_connection("default")
            redis_conn.hincrby(cart_key, product_id, 1)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        redis_conn.hdel(cart_key, product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)iew):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (JWTAuthentication,)

    def perform_create(self, serializer):
        user = self.get_user()
        if user:
            cart, created = Cart.objects.get_or_create(user=user)
        else:
            session_id = self.request.sessio(request):n.session_key
            if not session_id:
                self.request.session.cclass CartView(APIView):
    def get(self, request):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        cart_items = redis_conn.hgetall(cart_key)
        cart = {int(k.decode('utf-8')): int(v.decode('utf-8')) for k, v in cart_items.items()}
        return Response(cart)

    def post(self, request, product_id):
        product_service_url = f"http://product-service/api/products/{product_id}/"
        product_response = requests.get(product_service_url)
        if product_response.status_code == 200:
            cart_key = f"cart_{request.user.id}"
            redis_conn = get_redis_connection("default")
            redis_conn.hincrby(cart_key, product_id, 1)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        redis_conn.hdel(cart_key, product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)reate()
                session_id = self.request.session.session_key
            cart, created = Cart.objecclass CartView(APIView):
    def get(self, request):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        cart_items = redis_conn.hgetall(cart_key)
        cart = {int(k.decode('utf-8')): int(v.decode('utf-8')) for k, v in cart_items.items()}
        return Response(cart)

    def post(self, request, product_id):
        product_service_url = f"http://product-service/api/products/{product_id}/"
        product_response = requests.get(product_service_url)
        if product_response.status_code == 200:
            cart_key = f"cart_{request.user.id}"
            redis_conn = get_redis_connection("default")
            redis_conn.hincrby(cart_key, product_id, 1)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        redis_conn.hdel(cart_key, product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)ts.get_or_create(session_id=session_id)
        serializer.save(cart=cart)(request):
class CartView(APIView):
    def get(self, request):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        cart_items = redis_conn.hgetall(cart_key)
        cart = {int(k.decode('utf-8')): int(v.decode('utf-8')) for k, v in cart_items.items()}
        return Response(cart)

    def post(self, request, product_id):
        product_service_url = f"http://product-service/api/products/{product_id}/"
        product_response = requests.get(product_service_url)
        if product_response.status_code == 200:
            cart_key = f"cart_{request.user.id}"
            redis_conn = get_redis_connection("default")
            redis_conn.hincrby(cart_key, product_id, 1)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        redis_conn.hdel(cart_key, product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get_user(self):
        auth_header = self.request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            return jwt_auth.get_user(validated_token)
        return None

class MigrateCartView(views.APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')
        user = self.get_user()
        if session_id and user:
            try:class CartView(APIView):
    def get(self, request):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        cart_items = redis_conn.hgetall(cart_key)
        cart = {int(k.decode('utf-8')): int(v.decode('utf-8')) for k, v in cart_items.items()}
        return Response(cart)

    def post(self, request, product_id):
        product_service_url = f"http://product-service/api/products/{product_id}/"
        product_response = requests.get(product_service_url)
        if product_response.status_code == 200:
            cart_key = f"cart_{request.user.id}"
            redis_conn = get_redis_connection("default")
            redis_conn.hincrby(cart_key, product_id, 1)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id):
        cart_key = f"cart_{request.user.id}"
        redis_conn = get_redis_connection("default")
        redis_conn.hdel(cart_key, product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
                temp_cart = Cart.objects.get(session_id=session_id)
                user_cart, created = Cart.objects.get_or_create(user=user)
                for item in temp_cart.cartitem_set.all():
                    item.cart = user_cart
                    item.save()
                temp_cart.delete()
                return Response({'status': 'cart migrated successfully'})
            except Cart.DoesNotExist:
                return Response({'status': 'temporary cart not found'}, status=404)
        return Response({'status': 'invalid data'}, status=400)

    def get_user(self):
        auth_header = self.request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            return jwt_auth.get_user(validated_token)
        return None """

