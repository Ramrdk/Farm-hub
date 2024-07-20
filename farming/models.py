from django.db import models

# Create your models here.

    
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

    
    
    
class product(models.Model):
    description = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    quantity = models.CharField(max_length=150)
    prize = models.CharField(max_length=150)
    image = models.FileField(max_length=150)
    usertype = models.CharField(max_length=150)

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
    description = models.CharField(max_length=150)
    heading = models.CharField(max_length=150)
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
    