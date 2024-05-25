
import json
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
import requests
from rest_framework import viewsets, mixins , status
from .serializers import ProductSerializer
from .models import Product
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.exceptions import NotFound
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import requests
from django.conf import settings

class productView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductPageView(View):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        context = self.get_user_context(request)
        return render(request, 'products.html', context)

    def get_user_context(self, request):
        context = {}
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            jwt_auth = JWTAuthentication()
            try:
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
                context['username'] = user.username
            except InvalidToken:
                context['username'] = None
        else:
            context['username'] = None
        return context

class ProductDetailsView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'product_details.html', {'product': product})
    
def verifier_authentification(request):
    """
    Vérifie si l'utilisateur est authentifié. S'il ne l'est pas, redirige vers l'URL du microservice d'authentification.
    """
    if not request.user.is_authenticated:
        # Si l'utilisateur n'est pas authentifié, rediriger vers le service d'authentification
        return redirect(settings.AUTHENTICATION_MICROSERVICE_URL + '/auth/login/')  # Remplacez AUTHENTICATION_MICROSERVICE_URL par l'URL réelle du microservice d'authentification
    else:
        username = request.user.username
        return HttpResponse(f"Vous êtes déjà connecté en tant que {username}.")



def envoyer_produit_au_panier(product_id, user_id):
    """
    Envoie le produit au service "cart" en utilisant une requête HTTP POST.
    """
    # Construire l'URL de l'API du service "cart"
    cart_service_url = settings.CART_MICROSERVICE_URL + 'add/'  # Modifier en fonction de votre configuration

    # Données à envoyer dans la requête POST
    data = {
        'product_id': product_id,
        'user_id': user_id,
    }

    # Envoyer la requête POST à l'API du service "cart"
    response = requests.post(cart_service_url, data=data)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        print("Produit envoyé au panier avec succès!")
    else:
        print("Erreur lors de l'envoi du produit au panier:", response.text)


""" class CheckAuthenticationAndAddToCartView(APIView):
    def post(self, request):
        # Vérifier l'authentification de l'utilisateur
        redirect_url = verifier_authentification(request)
        if redirect_url:
            return redirect(redirect_url)

        # Si l'utilisateur est authentifié, envoyer le produit au service "cart"
        product_id = request.data.get('product_id')
        user_id = request.user.id
        envoyer_produit_au_panier(product_id, user_id)

        # Rediriger l'utilisateur vers la page d'accueil après avoir ajouté au panier
        return redirect('/') """

def add_to_cart(request,prodid):
            # Vérifier l'authentification de l'utilisateur
    #redirect_url = verifier_authentification(request)
    #if redirect_url:
        #return redirect(redirect_url)

        # Si l'utilisateur est authentifié, envoyer le produit au service "cart"
    product_id = prodid
    user_id = request.user.id
    envoyer_produit_au_panier(product_id, user_id)

        # Rediriger l'utilisateur vers la page d'accueil après avoir ajouté au panier
    return redirect('/products/')



def view_product(request,slug):
    product = Product.objects.get(slug=slug)
    if product:
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

def view_product1(request,id):
    product = Product.objects.get(pk=id)
    if product:
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

def index(request):
    return render(request, 'index.html')
