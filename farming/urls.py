"""farming URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


    


urlpatterns = [
    path('index.html',views.first,name='first'),
    path('',views.first,name='first'),
    path('customer',views.customer,name='customer'),
    path('track-order', views.track_order, name='track_order'),
    path('sellernew',views.sellernew,name='sellernew'),
    path('workernew',views.workernew,name='workernew'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('category',views.category,name='category'),
    path('addnews',views.addnews,name='addnews'),
    path('news',views.news,name='news'),
    path('login',views.login,name='login'),
    path('products',views.products,name='products'),
    path('admindash/',views.admindash, name='admindash'),
    path('homes/',views.homes, name='homes'),
    path('customeraddnew',views.customeraddnew, name='customeraddnew'),
    path('logint',views.logint, name='logint'),
    path('workeradd',views.workeradd, name='workeradd'),
    path('selleradd',views.selleradd, name='selleradd'),
    path('addworker',views.addworker, name='addworker'),
    path('addproduct',views.addproduct, name='addproduct'),
    path('purchase',views.purchase, name='purchase'),
    path('home',views.home, name='home'),
    path('viewproducts',views.viewproducts, name='viewproducts'),
    path('logout',views.logout, name='logout'),
    path('purchase/<int:id>',views.purchase, name='purchase'),
    path('purchase/addpayment',views.addpayment, name='addpayment'),
    path('purchaseview',views.purchaseview, name='purchaseview'),
    path('viewworkers',views.viewworkers, name='viewworkers'),
    path('viewfarmers',views.viewfarmers, name='viewfarmers'),
    path('viewcustomers',views.viewcustomers, name='viewcustomers'),
    path('pay',views.pay, name='pay'),
    path('homes',views.homes, name='homes'),
    path('homess',views.homess, name='homess'),
    path('viewnews',views.viewnews, name='viewnews'),
    path('viewworkernews',views.viewworkernews, name='viewworkernews'),
    path('addrequest/<int:id>',views.addrequest, name='addrequest'),
    path('addrequest/ress',views.ress, name='ress'),
    path('viewworkerrequest',views.viewworkerrequest, name='viewworkerrequest'),
    path('adminproduct',views.adminproduct, name='adminproduct'),
    path('addadminpro',views.addadminpro, name='addadminpro'),
    path('viewadminproductss',views.viewadminproductss, name='viewadminproductss'),
    path('viewworkersss',views.viewworkersss, name='viewworkersss'),

    path('insertproduct222',views.insertproduct222, name='insertproduct222'),
    path('workerprofile',views.workerprofile, name='workerprofile'),

    path('insertproduct',views.insertproduct, name='insertproduct'),
    path('addmachineryss',views.addmachineryss,name='addmachineryss'),
    path('adminmachinery',views.adminmachinery,name='adminmachinery'),
    path('viewworkermachinerys',views.viewworkermachinerys,name='viewworkermachinerys'),
    path('viewsellermachinerys',views.viewsellermachinerys,name='viewsellermachinerys'),
    
    path('sellerpurchase/<int:id>',views.sellerpurchase,name='sellerpurchase'),
    path('sellerpurchase/addpayment',views.addpayment,name='addpayment'),
    path('mechinarypurchase/<int:id>',views.mechinarypurchase,name='mechinarypurchase'),
    path('updateworkerprofile/<int:id>',views.updateworkerprofile,name='updateworkerprofile'),

        path('updateworkerprofile/editworkerprofile/<int:id>',views.editworkerprofile,name='editworkerprofile'),



        path('mechinarypurchase/addmachinarypurchase',views.addmachinarypurchase,name='addmachinarypurchase'),

    
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
