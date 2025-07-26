from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),  # ✅ chuyển Decimal thành float
            'quantity': 1,
        }

    request.session['cart'] = cart
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())  # ✅ float để chắc chắn
    return render(request, 'store/cart.html', {'cart': cart, 'total_price': total_price})

def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        cart = request.session.get('cart', {})
        products = Product.objects.filter(pk__in=cart.keys())

        order = Order.objects.create(name=name, email=email)

        for product in products:
            quantity = cart[str(product.pk)]['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        request.session['cart'] = {}  # Xóa giỏ hàng sau khi đặt
        return render(request, 'store/order_success.html', {'order': order})

    return render(request, 'store/checkout.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Đăng nhập sau khi đăng ký
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def order_success(request):
    return render(request, 'order_success.html')
