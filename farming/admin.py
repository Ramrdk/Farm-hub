from django.contrib import admin
from .models import (
    Order, addseller, admin as Admin, blockchainoutput, addworker,
    addcustomer, Product, payment, usercategory, usernews,
    seller_request, userproduct, machinery,Category,Subcategory
)
@admin.register(Order)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date', 'status', 'delivery_date')
    list_filter = ('status',)
    search_fields = ('order_date', 'status', 'delivery_date')


@admin.register(addseller)
class addsellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'email', 'phone')

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(blockchainoutput)
class BlockchainoutputAdmin(admin.ModelAdmin):
    list_display = ('output',)
    search_fields = ('output',)

@admin.register(addworker)
class AddworkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'experience', 'designation')
    search_fields = ('name', 'email', 'phone', 'designation')

@admin.register(addcustomer)
class AddcustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'email', 'phone')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'prize', 'usertype')
    search_fields = ('name', 'usertype')

@admin.register(payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'cid', 'prize', 'status')
    search_fields = ('name', 'cid', 'status')

@admin.register(usercategory)
class UsercategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    search_fields = ('category',)

@admin.register(usernews)
class UsernewsAdmin(admin.ModelAdmin):
    list_display = ('heading', 'date')
    search_fields = ('heading', 'date')

@admin.register(seller_request)
class SellerRequestAdmin(admin.ModelAdmin):
    list_display = ('heading', 'sid', 'name')
    search_fields = ('heading', 'sid', 'name')

@admin.register(userproduct)
class UserproductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'prize', 'usertype', 'category')
    search_fields = ('name', 'usertype', 'category')

@admin.register(machinery)
class MachineryAdmin(admin.ModelAdmin):
    list_display = ('name', 'des', 'prize')
    search_fields = ('name', 'des')



admin.site.register(Category)
admin.site.register(Subcategory)

