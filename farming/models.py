from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# for orders
from django.db import models
from django.core.files.base import ContentFile
from datetime import timedelta
import qrcode
import io

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Trsdetail(models.Model):
    # Your existing fields
    order_id = models.CharField(max_length=100, unique=True)
    user = models.PositiveIntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')
    address = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    order_notes = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=10, choices=[('Cash', 'Cash'), ('Card', 'Card'),('UPI', 'UPI')])
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)




    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.get_qr_code_data())
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        return ContentFile(buffer.getvalue(), 'order_qr_code.png')

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code = self.generate_qr_code()
        super().save(*args, **kwargs)

    def get_qr_code_data(self):
        # Customize this method to encode the information you need in the QR code
        return f"Order ID: {self.id}"
    
class Product(models.Model):
    product_id = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    quantity = models.CharField(max_length=150)
    prize = models.CharField(max_length=150)
    image = models.FileField(max_length=150)
    usertype = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=2)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE,default=2)


class Cart(models.Model):
    user = models.PositiveIntegerField()
    products = models.ManyToManyField(Product, through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.prize * self.quantity



class Order(models.Model):
    STATUS_CHOICES = [
        ('Order placed', 'Order placed'),
        ('Order Dispatched', 'Order Dispatched'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    ]
    order_id = models.CharField(max_length=100, unique=True)
    order_date = models.DateField()
    status = models.CharField(max_length=50, default='Order Placed',choices=STATUS_CHOICES)
    delivery_date = models.DateField()
    productname = models.CharField(max_length=150,default='20')
    quantity = models.CharField(max_length=150)
    price =models.CharField(max_length=150)
    
class addseller(models.Model):
    address = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    
    
class admin(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

class blockchainoutput(models.Model):
    output = models.CharField(max_length=150)
class addworker(models.Model):
    address = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    experience = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
 
    
    
class addcustomer(models.Model):
    address = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

    
    
    


class payment(models.Model):
    name = models.CharField(max_length=150)
    quantity = models.CharField(max_length=150)
    cid = models.CharField(max_length=150)
    prize = models.CharField(max_length=150)
    cardname = models.CharField(max_length=150)

    cardnumber = models.CharField(max_length=150)
    cardyear = models.CharField(max_length=150)
    cardtype = models.CharField(max_length=150)
    cardmonth = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    cvv = models.CharField(max_length=150)
    status = models.CharField(max_length=150)        
        
    
    
class usercategory(models.Model):
    category = models.CharField(max_length=150)
   
   
   
class usernews(models.Model):
    description = models.CharField(max_length=3000)
    heading = models.CharField(max_length=1500)
    date = models.CharField(max_length=150)
    image = models.FileField(max_length=150)
   
 
   
class seller_request(models.Model):
    description = models.CharField(max_length=150)
    heading = models.CharField(max_length=150)
    sid = models.CharField(max_length=150)
    name = models.CharField(max_length=150)

   
class userproduct(models.Model):
    description = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    quantity = models.CharField(max_length=150)
    prize = models.CharField(max_length=150)
    image = models.FileField(max_length=150)
    usertype = models.CharField(max_length=150)
    category = models.CharField(max_length=150)
    
    
    
    
    
class machinery(models.Model):
    name = models.CharField(max_length=150)
    des = models.CharField(max_length=150)
    image = models.FileField(max_length=150)
    prize = models.CharField(max_length=150)
    quantity = models.CharField(max_length=150)