from django import forms
from django.forms import ModelForm
from .models import payment
from .models import Product
from .models import usercategory
from .models import usernews
from .models import seller_request
from .models import userproduct

from django import forms
from .models import Category, Subcategory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Product Category'})
        }

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['category', 'name']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Product Subcategory'})
        }

class userpayment(forms.ModelForm):
    class Meta():

        model=payment
        fields="__all__"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'prize', 'description', 'image']        
        

class sellerproduct(forms.ModelForm):
    class Meta():

        model=Product
        fields="__all__"
        

class scategory(forms.ModelForm):
    class Meta():

        model=usercategory
        fields="__all__"
        
        
class newss(forms.ModelForm):
    class Meta():

        model=usernews
        fields="__all__"
        

class sellerre(forms.ModelForm):
    class Meta():

        model=seller_request
        fields="__all__"
        
        
class adminproducts(forms.ModelForm):
    class Meta():

        model=userproduct
        fields="__all__"
        
        
        
'''class machinery(forms.ModelForm):
    class Meta():

        model=machinerys
        fields="__all__" '''