import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required  # Профиль үшін керек


from .models import Product, Category, Brand, Review, Order, ContactMessage
from .forms import ProductForm


from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    ProductSerializer, CategorySerializer, BrandSerializer, 
    ReviewSerializer, OrderSerializer, ContactMessageSerializer
)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'main/signup.html'


@login_required
def profile(request):
    return render(request, 'main/profile.html')


def external_gadgets(request):
    url = "https://dummyjson.com/products/category/smartphones"
    external_items = []
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            external_items = response.json().get('products', [])
    except requests.exceptions.RequestException:
        external_items = []
    return render(request, 'main/external_api.html', {'external_items': external_items})


def index(request):
    latest_gadgets = Product.objects.all().order_by('id')[:6]
    return render(request, 'main/index.html', {'gadgets': latest_gadgets})

def catalog(request):
    cat_name = request.GET.get('cat')
    categories = Category.objects.all()
    if cat_name:
        products_list = Product.objects.filter(category__name=cat_name).order_by('id')
    else:
        products_list = Product.objects.all().order_by('id')

    paginator = Paginator(products_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/catalog.html', {
        'page_obj': page_obj, 
        'categories': categories,
        'cat_selected': cat_name
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'main/product_detail.html', {'product': product})

def contact(request):
    return render(request, 'main/contact.html')


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid(): 
            form.save()
            return redirect('catalog')
    else:
        form = ProductForm()
    return render(request, 'main/add_product.html', {'form': form, 'title': 'Жаңа тауар қосу'})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'main/add_product.html', {'form': form, 'title': 'Тауарды өңдеу'})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('catalog')


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    p_id = str(product_id)
    cart[p_id] = cart.get(p_id, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def cart(request):
    cart_session = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, quantity in cart_session.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({'product': product, 'quantity': quantity, 'total': item_total})
        except Product.DoesNotExist:
            continue
    return render(request, 'main/cart.html', {'cart_items': cart_items, 'total_price': total_price})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ReviewAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactMessageAPIView(APIView):
    def get(self, request):
        messages = ContactMessage.objects.all()
        serializer = ContactMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)