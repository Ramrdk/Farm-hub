# from .models import *
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import *
from django.contrib import messages
 
# FILE UPLOAD AND VIEW
from  django.core.files.storage import FileSystemStorage
# SESSION
from django.conf import settings
from .forms import *

data = None

from django.http import HttpResponse
from .import blockchain  
import json
from .models import Order
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Cart, CartItem
from django.contrib import messages
from .forms import ProductForm  # Assuming you have a ProductForm
import random
import string
import qrcode
import io
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


from django.shortcuts import render, redirect
from .models import Trsdetail, Order

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        order_id = request.session.get('order_id')

        if entered_otp == session_otp:
            # Fetch the Trsdetail entry with the given order_id
            tsrdetail = Trsdetail.objects.filter(order_id=order_id).first()
           
            
            if tsrdetail:
                # Update the Trsdetail status
                tsrdetail.status = 'Payment Completed'
                tsrdetail.save()

                # Create or update the Order entry
                order_date = tsrdetail.created_at
                delivery_date = order_date + timedelta(days=3)
            
              

                order, created = Order.objects.get_or_create(
                    order_id=tsrdetail.order_id,
                    defaults={
                        'order_date': order_date,
                        'delivery_date': delivery_date,
                        'status': 'Order Placed',
                         

                    }
                )

                # Update the Order status
                order.delivery_status = 'Payment Completed'
                order.save()

                # Clear session data
                del request.session['otp']
                del request.session['order_id']

                return render(request, 'payment_success.html', {'order': order})

        # If OTP is invalid
        return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    # For GET requests or if form submission fails, render the verify_otp page
    return render(request, 'verify_otp.html')

def place_order(request):
    
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.session['cid'])
        cart_items = CartItem.objects.filter(cart=cart)
        user = request.session['cid']
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        payment_method = request.POST.get('payment_method')
        print("--------------",payment_method)
        total_amount = sum(float(item.quantity) * float(item.product.prize) for item in cart_items)
        # Assuming cart_items is defined

        # Generate a unique order ID
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        print("-------------",order_id)
        # Create order
        order = Trsdetail.objects.create(
            user=user,
            order_id=order_id,
            total_amount=total_amount,
            address=address,
            city=city,
            state=state,
            #pincode=pincode,
            payment_method=payment_method,
            status='Pending'
        )

        # Generate QR code if payment method is UPI
        if payment_method == 'UPI':
            CartItem.objects.filter(cart_id=request.session['cid']).delete() 
            send_mail(      
            'Order Confirmation',
            f'Your order with order ID {order_id} has been placed successfully. Total amount: {total_amount}.',
            'from@example.com',
            [request.session['cemail']],
            fail_silently=False,            
        )
            print("-----------------upi")
            qr = qrcode.make(f'http://127.0.0.1:200/confirm_payment?order_id={order_id}')
            
            buffer = io.BytesIO()
            qr.save(buffer, 'PNG')
            order.qr_code.save(f'{order_id}.png', ContentFile(buffer.getvalue()), save=False)
            order.save()
            return redirect('order_success', order_id=order_id)
        elif payment_method == 'Card':
            CartItem.objects.filter(cart_id=request.session['cid']).delete() 
            send_mail(      
            'Order Confirmation',
            f'Your order with order ID {order_id} has been placed successfully. Total amount: {total_amount}.',
            'from@example.com',
            [request.session['cemail']],
            fail_silently=False,            
        )
            
            return   redirect('purchasego')
        
        elif payment_method == 'Cash':
            # Handle Cash payment (e.g., update order status to 'Cash on Delivery')
            print('fffff')
            CartItem.objects.filter(cart_id=request.session['cid']).delete() 
            send_mail(      
            'Order Confirmation',
            f'Your order with order ID {order_id} has been placed successfully. Total amount: {total_amount}.',
            'from@example.com',
            [request.session['cemail']],
            fail_silently=False,            
        )
            order.status = 'Cash on Delivery'
            order.save()     
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['order_id'] = order_id

            send_mail(
                'Order Confirmation - OTP',
                f'Your OTP for order {order_id} is {otp}.',
                'from@example.com',
                [request.session['cemail']],
                fail_silently=False,
            )
            return redirect('verify_otp')
              
        else:
                print("choose a valid payment option")         

         # Send order confirmation email
        # CartItem.objects.filter(cart_id=request.session['cid']).delete() 
         

    
    return render(request, 'checkout.html', {'cart_items': cart_items})

def confirm_payment_action(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Trsdetail, order_id=order_id)
        order.status = 'Payment Completed'
        order.save()
        
        return render(request, 'payment_success.html', {'order': order})
    
    return redirect('confirm_payment', order_id=order_id)

def confirm_payment(request):
    
    order_id = request.GET.get('order_id')
    if order_id:
        order = get_object_or_404(Trsdetail, order_id=order_id)
        order.status = 'Payment Completed'
        order.save()
        
        return render(request,'confirm_payment.html',{'order':order})
        
    return JsonResponse({'message': 'Invalid order ID.'}, status=400)

def order_success(request, order_id):
    # Fetch the Trsdetail record using the order_id
    order1 = Trsdetail.objects.get(order_id=order_id)
    
    tsrdetail = get_object_or_404(Trsdetail, order_id=order_id)
    
    # Calculate delivery date (3 days after the order date)
    order_date = tsrdetail.created_at
    delivery_date = order_date + timedelta(days=3)
   
    # Create or update the Order instance
    order, created = Order.objects.get_or_create(
        order_id=tsrdetail.order_id,
        defaults={
            'order_date': order_date,
            'delivery_date': delivery_date,
            'status': 'Order Placed',
            
            

        }
    )
    

    # Render the order_success.html template with the order details
    return render(request, 'order_success.html', {'order': order1})



def fetch_location_details(request):
    postcode = request.GET.get('postcode', '')
    if not postcode:
        return JsonResponse({'error': 'Postcode is required'}, status=400)

    try:
        url = f"https://api.postalpincode.in/pincode/{postcode}"
        response = requests.get(url,verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        if data:
            print(f"API Response: {data}")  # Debugging: Log API response
        else:
            print("No data received from API")  # Debugging: Log no data

        if data and data[0]['Status'] == 'Success':
            location_data = data[0]['PostOffice'][0]
            city = location_data['District']
            state = location_data['State']
            return JsonResponse({'city': city, 'state': state})
        else:
            return JsonResponse({'error': 'Invalid postcode or no data available'}, status=400)

    except requests.RequestException as e:
        print(f"RequestException: {e}")  # Debugging: Log exception details
        return JsonResponse({'error': 'Failed to fetch location details', 'details': str(e)}, status=500)
    
def selling_statistics(request):
    # Fetch order data
    orders = Product.objects.all().values('name', 'quantity', 'prize')  # Customize based on your models
    
    # Prepare data for the graph
    data = {
        'products': [],
        'quantities': [],
        'prices': []
    }

    for order in orders:
        data['products'].append(order['name'])
        data['quantities'].append(order['quantity'])
        data['prices'].append(order['prize'])

    return render(request, 'selling_statistics.html', {'data': json.dumps(data)})


def checkout(request):
    cart = Cart.objects.get(user=request.session['cid'])
    cart_items = CartItem.objects.filter(cart=cart)
    total_amount = sum(float(item.quantity) * float(item.product.prize) for item in cart_items)
    shipping_charge = 30.00
    gst = (total_amount * 12)/100

    grand_total = total_amount + shipping_charge +gst
    
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'shipping_charge': shipping_charge,
        'grand_total': grand_total,
        'gst': gst
    })

def product_catalog(request):
    query = request.GET.get('q', '')
    category_name = request.GET.get('category', '')
    subcategory_name = request.GET.get('subcategory', '')
    usertype = request.GET.get('usertype', '')

    # Get all products
    products = Product.objects.all()
    
    # Filter products based on the query parameters
    if query:
        products = products.filter(name__icontains=query)
    if category_name:
        products = products.filter(category__name=category_name)
    if subcategory_name:
        products = products.filter(subcategory__name=subcategory_name)
    if usertype:
        products = products.filter(usertype=usertype)

    # Get unique categories, subcategories, and usertypes
    categories = Category.objects.values_list('name', flat=True).distinct()
    subcategories = Subcategory.objects.values_list('name', flat=True).distinct()
    usertypes = Product.objects.values_list('usertype', flat=True).distinct()

    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
        'usertypes': usertypes,
    }
    
    return render(request, 'product_catalog.html', context)

def add_product(request):
    if request.user.is_authenticated and hasattr(request.user, 'seller'):
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.seller = request.user
                product.save()
                messages.success(request, 'Product added successfully!')
                return redirect('product_list')
            else:
                messages.error(request, 'Form is not valid. Please check the details.')
        else:
            form = ProductForm()
        return render(request, 'add_product.html', {'form': form})
    else:
        messages.error(request, 'You need to be logged in as a seller to add products.')
        return redirect('login')
    
def add_to_cart(request, product_id):
    #if 'cname' in request.session:
    if 'cid' in request.session:
        product = get_object_or_404(Product, product_id=product_id)
        print("----------",request.session['cid'])
        cart, created = Cart.objects.get_or_create(user=request.session['cid'])
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        messages.success(request, 'Product added to cart!')
        return redirect('cart_view')
        
    else:
        messages.error(request, 'You need to be logged in as a customer to add products to the cart.')
        return redirect('login')

def remove_from_cart(request, item_id):
    if 'cid' in request.session:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.session['cid'])
        cart_item.delete()
        messages.success(request, 'Product removed from cart!')
        return redirect('cart_view')
    else:
        messages.error(request, 'You need to be logged in to remove products from the cart.')
        return redirect('login')

def update_cart_quantity(request, item_id, action):
    if 'cid' in request.session:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.session['cid'])
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
            
            
        cart_item.save()
        return redirect('cart_view')
    else:
        messages.error(request, 'You need to be logged in to update the cart.')
        return redirect('login')

def cart_view(request):
    if 'cid' in request.session:
        cart, created = Cart.objects.get_or_create(user=request.session['cid'])
        cart_items = CartItem.objects.filter(cart=cart)
        return render(request, 'cart.html', {'cart_items': cart_items})
    else:
        messages.error(request, 'You need to be logged in as a customer to view the cart.')
        return redirect('login')


def purchasego(request):
    return render(request, 'purchase.html')


def purchase(request):
    if request.method == 'POST':
        # Extract card details (if needed)
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Simulate payment processing (without order_id validation)
        # For demonstration purposes, assume payment is always successful

        # Fetch the first 'Pending' order from Tsrdetail
        tsrdetail = Trsdetail.objects.filter(status='Pending').first()

        if tsrdetail:
            # Create or update Order entry
            order_date = tsrdetail.created_at
            delivery_date = order_date + timedelta(days=3)

            order, created = Order.objects.get_or_create(
                order_id=tsrdetail.order_id,
                defaults={
                    'order_date': order_date,
                    'delivery_date': delivery_date,
                    'status': 'Order Placed'
                }
            )

            # Update Order status to 'Payment Completed'
            order.delivery_status = 'Payment Completed'
            order.save()

            # Render the payment success page
            return render(request, 'payment_success.html', {'order': order})

        else:
            # If no orders with 'Pending' status found, redirect to checkout
            return redirect('checkout')

    # For GET requests or if form submission fails, render the purchase page
    return render(request, 'purchase.html')

def track_order(request):
    if request.method== 'POST':
        order_id=request.POST.get('order_id')
    order = get_object_or_404(Order, order_id=order_id)
    order_statuses = ['Order placed', 'Order Dispatched', 'Out for delivery', 'Delivered']
    current_index = order_statuses.index(order.status) if order.status in order_statuses else -1

    context = {
        'order': order,
        'order_statuses': order_statuses,
        'current_index': current_index
    }
    return render(request, 'track_order.html', context)
   
  
   







def create_tsrdetail(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        tsrdetail = Trsdetail.objects.create(order_id=order_id)
        print("-------------------------------jk")
        # Create corresponding Order instance
        order_date = tsrdetail.created_date
        delivery_date = order_date + timedelta(days=3)

        Order.objects.get_or_create(
            order_id=order_id,
            defaults={
                'order_date': order_date,
                'delivery_date': delivery_date,
                'delivery_status': 'Order Placed'
            }
        )

def all(request):
   
    all_products = Product.objects.all()  # Fetch the all products
    return render(request, 'shop.html', {'all_products': all_products})      

def first(request):
   
    top_products = Product.objects.all()[13:19]  # Fetch the top 3 products
    return render(request, 'index.html', {'top_products': top_products})





def addcategory(request):
    return render(request,'category.html')    
    


    
    
def customer(request):
    return render(request,'customer.html')
    

def sellernew(request):
    return render(request,'sellernew.html')
    
def workernew(request):
    return render(request,'workernew.html')
    
def homes(request):
    return render(request,'sellerdashboard.html')

    
def homess(request):
    return render(request,'workerdashboard.html')
    
def login(request):
    return render(request,'login.html')
    
    
def admindash(request):
    return render(request,'admin/index.html')
    
def products(request):
    
    admin=Product.objects.all()
    

    return render(request, 'shop.html',{'result':admin})
  
# def purchase(request):
#     admin=product.objects.all()
#     return render(request, 'shop.html',{'result':admin})
   

 
def homes(request):
    return render(request,'sellerdashbaord.html')
    
def insert(request):
    return render(request,'index.html')
    
def select(request):
    admin=product.objects.all()
    return render(request, 'shop.html',{'result':admin})
    
    
    
def logint(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if admin.objects.filter(email=email,password=password).exists():
        userdetail=admin.objects.get(email=email, password=password)
        print("admin-----------------")

        request.session['aid'] = userdetail.id
        request.session['admin'] = userdetail.name
        return render(request, 'index.html')
    
    
    

    elif addcustomer.objects.filter(email=email,password=password).exists():
        print("customer-----------------")
        userdetail=addcustomer.objects.get(email=email, password=password)
        if userdetail.password == request.POST['password']:
            request.session['cid'] = userdetail.id
            request.session['cname'] = userdetail.name

            request.session['cemail'] = email

            request.session['user'] = 'customer'
            print("index-----------------")

            return redirect(first)
            
            
    elif addseller.objects.filter(email=email,password=password).exists():
        print("seller-----------------")
        userdetails=addseller.objects.get(email=request.POST['email'], password=password)
        if userdetails.password == request.POST['password']:
            request.session['sid'] = userdetails.id
            request.session['sname'] = userdetails.name

            request.session['semail'] = email

            request.session['seller'] = 'seller'

            
            return render(request,'sellerdashbaord.html')
            
            
    elif addworker.objects.filter(email=email,password=password).exists():
        userdetails=addworker.objects.get(email=request.POST['email'], password=password)
        if userdetails.password == request.POST['password']:
            request.session['wid'] = userdetails.id
            request.session['wemail'] = email
            request.session['wname'] = userdetails.name

            request.session['worker'] = 'worker'

            
            return render(request,'sellerdashbaord.html')

    else:
        messages.error(request, "Invalid password ")
        return render(request, 'index.html', {'status': 'failed'})    
    
    
    
    
    
    
    
    
    
'''   
def customerlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    

    if addcustomer.objects.filter(email=email,password=password).exists():
        customerdetail=addcustomer.objects.get(email=request.POST['email'], password=password)
        request.session['cid'] = customerdetail.id
        request.session['email'] = customerdetail.email
        return redirect(products)
    
    else:
        return render(request, 'login.html', {'status': 'failed'})


def sellerlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    

    if addseller.objects.filter(email=email,password=password).exists():
        sellerdetail=addseller.objects.get(email=request.POST['email'], password=password)
        request.session['sid'] = sellerdetail.id
        request.session['email'] = sellerdetail.email
        return render(request, 'sellerdashbaord.html', {'status': 'success'})
    
    else:
        return render(request, 'sellerlogin.html', {'status': 'failed'})
        
        
        
        
def workerlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    

    if addworker.objects.filter(email=email,password=password).exists():
        workerdetail=addworker.objects.get(email=request.POST['email'], password=password)
        request.session['wid'] = workerdetail.id
        request.session['email'] = workerdetail.email
        return render(request, 'workerdashboard.html', {'status': 'success'})
    
    else:
        return render(request, 'workerlogin.html', {'status': 'failed'})'''
        
        
def workerprofile(request):
    if request.session.has_key('wid'):
        user = addworker.objects.get(id=request.session['wid'])
        return render(request, 'workerprofile.html', {'result': user, 'profile_type': 'worker'})
    elif request.session.has_key('cid'):
        customer = addcustomer.objects.get(id=request.session['cid'])
        return render(request, 'workerprofile.html', {'result': customer, 'profile_type': 'customer'})
    elif request.session.has_key('sid'):
        seller = addseller.objects.get(id=request.session['sid'])
        return render(request, 'workerprofile.html', {'result': seller, 'profile_type': 'seller'})
    else:
        return redirect('first')  # Redirect to index page if no relevant session key
        
    
def selleradddata(request):
    if request.method == 'POST':
        #a1=request.POST.get('name')
        #a1=request.POST.get('name')
        a1=5
        a2=request.POST.get('address')
        a3=request.POST.get('email')
        a4=request.POST.get('phone')
        a5=request.POST.get('password')
        formdata=addseller(name=a1,address=a2,email=a3,phone=a4,password=a5)
        #formdata=addcustomer(name=a1,address=a2,email=a3,phone=a4,password=a5)
        #formdata=product(name=a2,description=a2,quantity=a2,prize=a4)
        formdata.save()
        return render(request, 'seller.html')
    else:
        return render(request,'index.html')
        
        
    


def customeraddnew(request):
    if request.method == 'POST':
        #a1=request.POST.get('name')
        a1=request.POST.get('name')
        a2=request.POST.get('address')
        a3=request.POST.get('email')
        a4=request.POST.get('phone')
        a5=request.POST.get('password')
        # a6=request.POST.get('gender')
        # a7=request.POST.get('dob')
        formdata=addcustomer(name=a1,address=a2,email=a3,phone=a4,password=a5)
        #formdata=product(name=a2,description=a2,quantity=a2,prize=a4)
        formdata.save()
        return render(request, 'login.html')
    else:
        return render(request,'index.html')
    


def selleradd(request):
    if request.method == 'POST':
        #a1=request.POST.get('name')
        a1=request.POST.get('name')
        a2=request.POST.get('address')
        a3=request.POST.get('email')
        a4=request.POST.get('phone')
        a5=request.POST.get('password')
        formdataaa=addseller(address=a2,name=a1,email=a3,phone=a4,password=a5)
        #formdata=product(name=a2,description=a2,quantity=a2,prize=a4)
        formdataaa.save()
        return render(request, 'login.html')
    else:
        return render(request,'index.html')
    


def workeradd(request):
    if request.method == 'POST':
        #a1=request.POST.get('name')
        a1=request.POST.get('name')
        a2=request.POST.get('address')
        a3=request.POST.get('email')
        a4=request.POST.get('phone')
        a5=request.POST.get('password')
        a6=request.POST.get('experience')
        a7=request.POST.get('designation')
        formdataaa=addworker(address=a2,name=a1,email=a3,phone=a4,password=a5,experience=a6,designation=a7)
        #formdata=product(name=a2,description=a2,quantity=a2,prize=a4)
        formdataaa.save()
        return render(request, 'login.html')
    else:
        return render(request,'index.html')
    

def home(request):
    return render(request, 'workerdashboard.html')


def addproduct(request):
    if request.session.has_key('sname'):
        temp=request.session['sname']
        users = addseller.objects.get(name=request.session['sname'])
        print(temp)

    return render(request,'addproduct.html',{'res':temp})


def insertproduct222(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = sellerproduct( request.POST,request.FILES)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'addproduct.html')
    else:
        # GET, generate unbound (blank) form
        form = sample_insert()
        return render(request,'index.html')


def insertproduct(request):
    if request.method == 'POST':
        a1=request.POST.get('name')
        a2=request.POST.get('description')
        a3=request.POST.get('quantity')
        a4=request.POST.get('prize')
        a5=request.POST.get('usertype')
        a6=request.POST.get('Category')
        a7=request.POST.get('Subcategory')
        product_id =request.POST.get('product_id')
        print(a1)
        print(a2)
        print(a3)
        print(a4)
        print(a5)
        myfile=request.FILES['myfile']
        print(myfile)
        fs= FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        formdata=Product(product_id=product_id,name=a1,description=a2,quantity=a3,prize=a4,image=filename,usertype=a5,category_id =a6,subcategory_id=a7)
        formdata.save()
        messages.success(request,   "Product Added succesfully")
        
        return render(request, 'addproduct.html')
    else:
        return render(request,'index.html')



# def insertproduct(request):
    # form = product()
    # if request.method=='POST':
        # name=request.POST.get('name')
        # print(name)
        # form = sample_insert(request.POST,request.FILES)
        # if form.is_valid():
            # form.save()
        # return render(request,'addproduct.html')
    # else:

        # return render(request, 'index.html')

"""

def insertproduct(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        quantity=request.POST.get('quantity')\
        image=request.POST.get(image)
        
        uploaded_file = request.FILES['document']
        print(uploaded_file)
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        
        data=product(image=uploaded_file)
        data.save()
    return render(request, 'addproduct.html', context)
"""

    
def viewproducts(request):
    users=Product.objects.all()
    
  
    return render(request,'viewproducts.html',{'res':users})
    
def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(first) 
    
    
    
# def purchase(request,id):
#     users=product.objects.get(id=id)
#     if request.session.has_key('cname'):
#             temp=request.session['cname']
#             pro = addcustomer.objects.get(name=request.session['cname'])
#             print(temp)
    
#     return render(request,'purchase.html',{'res':users,'res1':temp})

    
def addpayment(request):
    if request.method == 'POST':
        name=request.POST['name']
        cardname=request.POST['cardname']
        cardnumber=request.POST['cardnumber']
        quantity=int(request.POST['quantity'])
        amount=int(request.POST['prize'])
        cid=request.POST['cid']
        cardtype=request.POST['cardtype']
        cardyear=request.POST['cardyear']
        cardmonth=request.POST['cardmonth']
        cvv=request.POST['cvv']
        date=request.POST['date']
        status=request.POST['status']
        c=quantity*amount
        
        # POST, generate bound form with data from the request
        block_chain = blockchain.Block_chain()  
        transaction1 = block_chain.newTransaction(name,cardname,cardnumber)  
 
        block_chain.newBlock(10123)  

  
        print("Genesis block: ", block_chain.chain)
        temp=userproduct.objects.get(name=name)
        k=temp.name
        l=temp.description
        m=int(temp.quantity)
        n=temp.prize
        id=temp.id
        o=temp.image
        p=temp.usertype
        q=m-quantity
        if quantity >= m:
            return render(request,'purchase.html',{'status':'out of stock'})
        else:
        # POST, generate bound form with data from the request
            users=payment(name=name,cardname=cardname,cardnumber=cardnumber,quantity=quantity,prize=c,cid=cid,cardtype=cardtype,cardyear=cardyear,cardmonth=cardmonth,cvv=cvv,date=date,status=status)
            users.save()
            
            formdata=product(name=k,description=l,quantity=q,prize=n,image=o,usertype=p,id=id)
            formdata.save()
            return redirect(products)
    else:


        # GET, generate unbound (blank) form
        return render(request,'purchase.html')
        
  
def purchaseview(request):
    userss=Trsdetail.objects.all()

    
  
    return render(request,'purchaseview.html',{'res':userss})
    
def viewworkers(request):
    users=addworker.objects.all()
    
  
    return render(request,'viewworker.html',{'res':users})
    
    
def viewworkersss(request):
    users=addworker.objects.all()
    
  
    return render(request,'viewworkerss.html',{'res':users})
    
def viewfarmers(request):
    users=addseller.objects.all()
    
  
    return render(request,'viewfarmers.html',{'res':users})
    
    
def viewcustomers(request):
    users=addcustomer.objects.all()
    
  
    return render(request,'viewcustomerss.html',{'res':users})
    
def pay(request):
    users=payment.objects.all()
    
  
    return render(request,'viewpay.html',{'res':users})

'''def sellerrequest(request):
    users=addworker.objects.all()
    
  
    return render(request,'request.html',{'res':users})'''
    
    

def category_view(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        subcategory_form = SubcategoryForm(request.POST)
        
        if category_form.is_valid() and subcategory_form.is_valid():
            # Save the category and subcategory
            category = category_form.save()
            subcategory = subcategory_form.save(commit=False)
            subcategory.category = category
            subcategory.save()
            messages.success(request, 'Category added successfully!')
            return redirect('index.html')
           
          # Redirect to a success page or another view
    else:
        category_form = CategoryForm()
        subcategory_form = SubcategoryForm()

    return render(request, 'category.html', {
        'category_form': category_form,
        'subcategory_form': subcategory_form
    })
        
        
def addnews(request):
    
    return render(request,'news.html')
    
def news(request):
    
    return render(request,'news.html')
    
def sellerpurchase(request,id):
    users=userproduct.objects.get(id=id)
    if request.session.has_key('sname'):
            temp=request.session['sname']
            pro = addseller.objects.get(name=request.session['sid'])
            print('------------------------')
            print(temp)
    
    return render(request,'sellerpurchase.html',{'res':users,'res1':temp})

    
    

        
def news(request):
    if request.method == "POST":
        a=request.POST.get('heading')
        b=request.POST.get('description')
        myfile=request.FILES['image']
        fs= FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        d=request.POST.get('date')
        user=usernews(heading=a,description=b,image=myfile,date=d)
        user.save()
        return render(request,'news.html',{'status':'Successfully Added'})
                
    
def viewnews(request):
    users=usernews.objects.all()
    
  
    return render(request,' ',{'res':users})
    
    
    
def viewworkernews(request):
    users=usernews.objects.all()
    
  
    return render(request,'viewworkernews.html',{'res':users})
    
    
def addrequest(request,id):
    users=addworker.objects.get(id=id)
    b=users.name
    print(b)
    
    if request.session.has_key('sid'):
        temp=request.session['sid']
        users = addseller.objects.get(id=request.session['sid'])
        print(temp)
        a=users.name
        print(a)


  
    return render(request,'request.html',{'res':b,'res1':a})



    
def ress(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = sellerre(request.POST,request.FILES)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'request.html')
    else:
        # GET, generate unbound (blank) form
        form = seller_request()
        return render(request,'request.html')
        
        
        
        
        
   
def viewworkerrequest(request):
    if request.session.has_key('wname'):
        temp=request.session['wname']
        users = seller_request.objects.filter(name=request.session['wname'])
        
    return render(request,'viewworkerrequest.html',{'res':users})
    
    

    
   
def adminproduct(request):
    if request.session.has_key('admin'):
        temp=request.session['admin']
        users = admin.objects.get(name=request.session['admin'])
        print(temp)
        user=usercategory.objects.all()

    return render(request,'adminproduct.html',{'res':temp,'res1':user})
    


def addadminpro(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = adminproducts(request.POST,request.FILES)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'adminproduct.html')
    else:
        # GET, generate unbound (blank) form
        form = userproduct()
        return render(request,'adminproduct.html')
        
        
def viewadminproductss(request):
    
    admin=Product.objects.all()
    return render(request, 'adminproducts.html',{'result':admin})
    
    
    
    
    
def addmachineryss(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        prize=request.POST.get('prize')
        
       
        image=request.FILES['image']
     
        fs= FileSystemStorage()
        image=fs.save(image.name,image)
        formdata=machinery(name=name,des=description,prize=prize,image=image)
        formdata.save()
        return render(request, 'addmachinerytools.html')
    else:
        return render(request,'index.html')



def adminmachinery(request):
    
    return render(request,'addmachinerytools.html')
    
    
    
    
    
    
def viewworkermachinerys(request):
    users=machinery.objects.all()
    
  
    return render(request,'viewworkermachinery.html',{'res':users})
    

def viewsellermachinerys(request):
    users=machinery.objects.all()
    
  
    return render(request,'viewsellermachinery.html',{'res':users})
    



def mechinarypurchase(request,id):
    users=machinery.objects.get(id=id)
    if request.session.has_key('sname'):
            temp=request.session['sname']
            pro = addseller.objects.get(name=request.session['sname'])
            print(temp)
    
    return render(request,'mechinarypurchase.html',{'res':users,'res1':temp})


def addmachinarypurchase(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        prize=request.POST.get('prize')
        cardname=request.POST.get('cardname')
        cardnumber=request.POST.get('cardnumber')
        cardtype=request.POST.get('cardtype')
        cardyear=request.POST.get('cardyear')
        cardmonth=request.POST.get('cardmonth')
        cvv=request.POST.get('cvv')
        date=request.POST.get('date')
        cid=request.POST.get('cid')
        status=request.POST.get('status')

        
        
        formdata=payment(name=name,prize=prize,cardname=cardname,cardnumber=cardnumber,cardtype=cardtype,cardyear=cardyear,cardmonth=cardmonth,cvv=cvv,date=date,cid=cid,status=status)
        formdata.save()
        return render(request, 'mechinarypurchase.html')
    else:
        return render(request,'index.html')


def editworkerprofile(request,id):
    if request.method == 'POST':
        name=request.POST.get('name')
        address=request.POST.get('address')
        experience=request.POST.get('experience')
        designation=request.POST.get('designation')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phone=request.POST.get('phone')
       
        
        
        formdata=addworker(name=name,address=address,experience=experience,designation=designation,password=password,phone=phone,id=id,email=email)
        formdata.save()
        return redirect('workerprofile')
        
    updateworkerprofile.html
    
   
def updateworkerprofile(request,id):
    users=addworker.objects.get(id=id)
    
  
    return render(request,'updateworkerprofile.html',{'res':users})

def updatecustomerprofile(request,id):
    users=addcustomer.objects.get(id=id)
    
  
    return render(request,'updateworkerprofile.html',{'res':users})