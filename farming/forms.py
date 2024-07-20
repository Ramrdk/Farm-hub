from django import forms
from django.forms import ModelForm
from .models import payment
from .models import product
from .models import usercategory
from .models import usernews
from .models import seller_request
from .models import userproduct


class userpayment(forms.ModelForm):
    class Meta():

        model=payment
        fields="__all__"
        

class sellerproduct(forms.ModelForm):
    class Meta():

        model=product
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