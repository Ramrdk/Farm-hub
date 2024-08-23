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
from .views import  fetch_location_details
from django.conf import settings
from django.conf.urls.static import static


    


urlpatterns = [
    path('index.html',views.first,name='first'),
    path('',views.first,name='first'),
    path('catalog/',views.product_catalog, name='product_catalog'),
    path('selling-statistics/', views.selling_statistics, name='selling_statistics'),
    path('shop.html',views.all,name='all'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_product/', views.add_product, name='add_product'),
    path('cart/', views.cart_view, name='cart_view'),
    path('confirm_payment/',views.confirm_payment, name='confirm_payment'),
    path('confirm_payment_action/<str:order_id>/', views.confirm_payment_action, name='confirm_payment_action'),
    path('order_success/<str:order_id>/',views. order_success, name='order_success'),
    path('add_to_cart/<str:product_id>/',views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('purchasego', views.purchasego, name='purchasego'),
    path('update_cart_quantity/<int:item_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/<str:order_id>/', views.order_success, name='order_success'),
    #path('checkout/', views.checkout, name='checkout'),
    #path('product_list/', views.product_list, name='product_list'),
    path('track-order', views.track_order, name='track_order'),
    path('customer',views.customer,name='customer'),
    path('cart',views.cart_view,name='cart'),
    path('track-order', views.track_order, name='track_order'),
    path('sellernew',views.sellernew,name='sellernew'),
    path('workernew',views.workernew,name='workernew'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('category',views.category_view,name='category_view'),
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
    #path('purchase',views.add_to_cart, name='purchase'),
    path('home',views.home, name='home'),
    path('fetch_location_details/',fetch_location_details, name='fetch_location_details'),
    path('viewproducts',views.viewproducts, name='viewproducts'),
    path('logout',views.logout, name='logout'),
    path('purchase/',views.purchase , name='purchase'),
    #path('purchase/addpayment',views.addpayment, name='addpayment'),
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
    path('updatecustomerprofile/<int:id>',views.updatecustomerprofile,name='updatecustomerprofile'),
    path('updateworkerprofile/<int:id>',views.updateworkerprofile,name='updateworkerprofile'),

        path('updateworkerprofile/editworkerprofile/<int:id>',views.editworkerprofile,name='editworkerprofile'),



        path('mechinarypurchase/addmachinarypurchase',views.addmachinarypurchase,name='addmachinarypurchase'),

    
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

    
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
