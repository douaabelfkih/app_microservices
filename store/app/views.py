from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request, 'index.html')

def item(request,slug):
    return render(request, 'product.html', {'slug': slug})

def cart(request):
    return render(request, 'cart.html')

def orders(request):
    return render(request, 'orders.html')

