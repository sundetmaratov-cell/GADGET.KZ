from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория атауы")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категориялар"

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Бренд атауы")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Брендтер"

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Тауар атауы")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Бағасы")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Бренд")
    description = models.TextField(verbose_name="Сипаттама") 
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Сурет") 
    specs = models.TextField(null=True, blank=True, verbose_name="Техникалық сипаттамалар") 
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тауар"
        verbose_name_plural = "Тауарлар"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Тауар")
    text = models.TextField(verbose_name="Пікір мәтіні")
    rating = models.IntegerField(verbose_name="Рейтинг (1-5)")

    class Meta:
        verbose_name = "Пікір"
        verbose_name_plural = "Пікірлер"

class Order(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name="Тапсырыс беруші")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Уақыты")

    class Meta:
        verbose_name = "Тапсырыс"
        verbose_name_plural = "Тапсырыстар"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Тапсырыс")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Тауар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Саны")

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Аты-жөні")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Тақырыбы")
    message = models.TextField(verbose_name="Хабарлама")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Хабарлама"
        verbose_name_plural = "Хабарламалар"