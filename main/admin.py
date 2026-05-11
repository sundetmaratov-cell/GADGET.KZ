from django.contrib import admin
from .models import Category, Brand, Product, Review, Order, OrderItem, ContactMessage

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price') 
    list_filter = ('category', 'brand')
    search_fields = ('name', 'description') 
    ordering = ('price',) 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'date')
    inlines = [OrderItemInline] 

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Review)
admin.site.register(ContactMessage)
