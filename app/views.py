from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, Customer, Cart, OrderPlaced, SearchHistory
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db. models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'totalitem': totalitem})

class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = get_object_or_404(Product, pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'product_id': pk, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)
    # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    cart_item = Cart.objects.filter(product=product, user=user).first()
    if cart_item:
        # Nếu đã có, tăng số lượng lên 1
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Nếu chưa có, thêm mới vào giỏ hàng
        Cart.objects.create(user=user, product=product, quantity=1)
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        totalitem = len(cart)
        if cart.exists():
            for item in cart:
                tempamount = (item.quantity * item.product.discounted_price)
                amount += tempamount
            total_amount = amount + shipping_amount
        else:
            return render(request, 'app/emptycart.html', {'totalitem': totalitem})

        return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': total_amount, 'amount': amount, 'totalitem': totalitem})
    else:
        return render(request, 'app/addtocart.html', {'carts': [], 'totalamount': 0, 'amount': 0, 'totalitem': 0})

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart_item.quantity += 1
        cart_item.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            tempamount = (item.quantity * item.product.discounted_price)
            amount += tempamount
        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            cart_item.quantity = 0
            amount = 0.0
            shipping_amount = 70.0
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                tempamount = (item.quantity * item.product.discounted_price)
                amount += tempamount
            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount
            }
            return JsonResponse(data)
        amount = 0.0
        shipping_amount = 70.0
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            tempamount = (item.quantity * item.product.discounted_price)
            amount += tempamount
        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart_item.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            tempamount = (item.quantity * item.product.discounted_price)
            amount += tempamount
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op})

def mobile(request, data=None):
    if data is None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'iPhone':
        mobiles = Product.objects.filter(category='M', title__icontains='iPhone')
    elif data == 'Oppo':
        mobiles = Product.objects.filter(category='M', title__icontains='Oppo')
    elif data == 'Samsung':
        mobiles = Product.objects.filter(category='M', title__icontains='Samsung')
    elif data == 'Xiaomi':
        mobiles = Product.objects.filter(category='M', title__icontains='Xiaomi')
    elif data == 'Realmi':
        mobiles = Product.objects.filter(category='M', title__icontains='Realmi')
    elif data == 'Vivo':
        mobiles = Product.objects.filter(category='M', title__icontains='Vivo')
    elif data == 'below':
        mobiles = Product.objects.filter(category='M', discounted_price__lte=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M', discounted_price__gt=10000)
    else:
        mobiles = Product.objects.none()
    print(f"Filter data: {data}")
    print(f"Products: {mobiles}")
    return render(request, 'app/mobile.html', {'mobiles':  mobiles})

def laptop(request, data=None):
    if data is None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Dell':
        laptops = Product.objects.filter(category='L', title__icontains='Dell')
    elif data == 'Lenovo':
        laptops = Product.objects.filter(category='L', title__icontains='Lenovo')
    elif data == 'HP':
        laptops = Product.objects.filter(category='L', title__icontains='HP')
    elif data == 'Asus':
        laptops = Product.objects.filter(category='L', title__icontains='Asus')
    elif data == 'Acer':
        laptops = Product.objects.filter(category='L', title__icontains='Acer')
    elif data == 'MSI':
        laptops = Product.objects.filter(category='L', title__icontains='MSI')
    elif data == 'below':
        laptops = Product.objects.filter(category='L', discounted_price__lte=15000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L', discounted_price__gt=15000)
    else:
        laptops = Product.objects.none()
    print(f"Filter data: {data}")
    print(f"Products: {laptops}")
    return render(request, 'app/laptop.html', {'laptops': laptops})


def topwear(request, data=None):
    if data is None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Nam':
        topwears = Product.objects.filter(category='TW', title__icontains='Nam')
    elif data == 'Nữ':
        topwears = Product.objects.filter(category='TW', title__icontains='Nữ')
    elif data == 'Quần':
        topwears = Product.objects.filter(category='TW', title__icontains='Quần')
    elif data == 'Áo':
        topwears = Product.objects.filter(category='TW', title__icontains='Áo')
    elif data == 'below':
        topwears = Product.objects.filter(category='TW', discounted_price__lte=300)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW', discounted_price__gt=300)
    else:
        topwears = Product.objects.none()
    print(f"Filter data: {data}")
    print(f"Products: {topwears}")
    return render(request, 'app/topwear.html', {'topwears':  topwears})

def bottomwear(request, data=None):
    if data is None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'Nam':
        bottomwears = Product.objects.filter(category='BW', title__icontains='Nam')
    elif data == 'Nữ':
        bottomwears = Product.objects.filter(category='BW', title__icontains='Nữ')
    elif data == 'Quần':
        bottomwears = Product.objects.filter(category='BW', title__icontains='Quần')
    elif data == 'Áo':
        bottomwears = Product.objects.filter(category='BW', title__icontains='Áo')
    elif data == 'below':
        bottomwears = Product.objects.filter(category='BW', discounted_price__lte=300)
    elif data == 'above':
        bottomwears = Product.objects.filter(category='BW', discounted_price__gt=300)
    else:
        bottomwears = Product.objects.none()  # Trả về không có sản phẩm nếu `data` không hợp lệ
    print(f"Filter data: {data}")
    print(f"Products: {bottomwears}")
    return render(request, 'app/bottomwear.html', {'bottomwears': bottomwears})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chúc mừng bạn đã đăng ký thành công')
            return redirect('login')  # Chuyển hướng sau khi đăng ký thành công
        return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0

    for p in cart_items:
        tempamount = p.quantity * p.product.discounted_price
        amount += tempamount

    total_amount = amount + shipping_amount

    return render(request, 'app/checkout.html', {
        'add': add,
        'totalamount': total_amount,
        'cart_items': cart_items,
    })

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart =  Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations ! Profile Update Successfully !')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
    
def buy_now(request):
    return render(request, 'app/buynow.html')

def securitypolicy_view(request):
   return render(request, 'app/securitypolicy.html')

def about_view(request):
   return render(request, 'app/about.html')

@login_required
def search_history(request):
    history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')
    unique_queries = []
    seen_queries = set()
    for item in history:
        if item.query not in seen_queries:
            unique_queries.append(item)
            seen_queries.add(item.query)
            if len(unique_queries) == 6:
                break
    return render(request, 'app/search_history.html', {'history': unique_queries})

def search(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(title__icontains=query) if query else Product.objects.none()
    
    # Nếu người dùng đã đăng nhập, lưu lịch sử tìm kiếm
    if request.user.is_authenticated:
        if query:
            SearchHistory.objects.create(user=request.user, query=query)
        
        # Trả về lịch sử tìm kiếm
        history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')
        unique_queries = []
        seen_queries = set()
        for item in history:
            if item.query not in seen_queries:
                unique_queries.append(item)
                seen_queries.add(item.query)
                if len(unique_queries) == 6:
                    break
    else:
        unique_queries = []
    
    return render(request, 'app/search_results.html', {'results': results, 'query': query, 'history': unique_queries})

@csrf_exempt
def save_search_history(request):
    if request.method == 'POST' and request.user.is_authenticated:
        query = request.POST.get('query', '')
        if query:
            SearchHistory.objects.create(user=request.user, query=query)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def get_search_history(request):
    if request.user.is_authenticated:
        history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')
        unique_queries = []
        seen_queries = set()
        for item in history:
            if item.query not in seen_queries:
                unique_queries.append(item.query)
                seen_queries.add(item.query)
                if len(unique_queries) == 6:
                    break
        return JsonResponse({'history': unique_queries})
    else:
        # Trả về lịch sử tìm kiếm trống nếu người dùng chưa đăng nhập
        return JsonResponse({'history': []})