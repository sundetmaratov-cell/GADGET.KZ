from django import forms
from django.contrib.auth.models import User  
from .models import Product, Review

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Пароль"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, 
        label="Парольді қайталаңыз"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Парольдер сәйкес келмейді!")
        return cleaned_data

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'brand', 'description', 'image', 'specs']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Баға нөлден жоғары болуы керек!")
        return price