# from django.http import HttpResponse
# from django.http import HttpResponse
# from django.shortcuts import render

# from .models import *

# from django.core.files.storage import FileSystemStorage
from django.db.models import Q

from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
# FILE UPLOAD AND VIEW
from  django.core.files.storage import FileSystemStorage
# SESSION
from django.conf import settings

from .forms import *

data = None

from .forms import *

from .import blockchain  

def first(request):
    return render(request,'index.html')
    
def addcategory(request):
    return render(request,'category.html')    
    
def track_order(request):
    print('Testing')
    return render(request,'track_order.html') 

    
    
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
    admin=product.objects.filter(~Q(quantity=0))

    return render(request, 'shop.html',{'result':admin})
  
def purchase(request):
    admin=product.objects.all()
    return render(request, 'shop.html',{'result':admin})
   

 
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

        request.session['aid'] = userdetail.id
        request.session['admin'] = userdetail.name
        return render(request, 'index.html')

    elif addcustomer.objects.filter(email=email,password=password).exists():
        userdetail=addcustomer.objects.get(email=email, password=password)
        if userdetail.password == request.POST['password']:
            request.session['cid'] = userdetail.id
            request.session['cname'] = userdetail.name

            request.session['cemail'] = email

            request.session['user'] = 'customer'

            
            return render(request, 'index.html')
    elif addseller.objects.filter(email=email,password=password).exists():
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

            
            return render(request,'workerdashboard.html')

    else:
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
        temp=request.session['wid']
        user = addworker.objects.get(id=request.session['wid'])
        # us=[]
        # us['id']=user.id
        # email= user.email

        return render(request,'workerprofile.html',{'result': user})

        
    
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
        formdata=addcustomer(name=a1,address=a2,email=a3,phone=a4,password=a5)
        #formdata=product(name=a2,description=a2,quantity=a2,prize=a4)
        formdata.save()
        return render(request, 'worker.html')
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
        return render(request, 'worker.html')
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
        return render(request, 'workernew.html')
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
        print(a1)
        print(a2)
        print(a3)
        print(a4)
        print(a5)
        myfile=request.FILES['myfile']
        print(myfile)
        fs= FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        formdata=product(name=a1,description=a2,quantity=a3,prize=a4,image=filename,usertype=a5)
        formdata.save()
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
    users=product.objects.all()
    
  
    return render(request,'viewproducts.html',{'res':users})
    
def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(first) 
    
    
    
def purchase(request,id):
    users=product.objects.get(id=id)
    if request.session.has_key('cname'):
            temp=request.session['cname']
            pro = addcustomer.objects.get(name=request.session['cname'])
            print(temp)
    
    return render(request,'purchase.html',{'res':users,'res1':temp})

    
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
    userss=payment.objects.all()

    
  
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
    
    
def category(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = scategory( request.POST)
        # check if it's valid:
        if form.is_valid():
        #Insert into DB
            form.save()
        #redirect to a new URL:
            return render(request, 'category.html')
    else:
        # GET, generate unbound (blank) form
        form = usercategory()
        return render(request,'category.html')
        
        
def addnews(request):
    
    return render(request,'news.html')
    
def news(request):
    
    return render(request,'news.html')
    
def sellerpurchase(request,id):
    users=userproduct.objects.get(id=id)
    if request.session.has_key('sname'):
            temp=request.session['sname']
            pro = addseller.objects.get(name=request.session['sname'])
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
    
  
    return render(request,'viewsnews.html',{'res':users})
    
    
    
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
    admin=userproduct.objects.all()
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
        password=request.POST.get('password')
        phone=request.POST.get('phone')
       
        
        
        formdata=addworker(name=name,address=address,experience=experience,designation=designation,password=password,phone=phone,id=id)
        formdata.save()
        return redirect('workerprofile')
        
    updateworkerprofile.html
    
   
def updateworkerprofile(request,id):
    users=addworker.objects.get(id=id)
    
  
    return render(request,'updateworkerprofile.html',{'res':users})