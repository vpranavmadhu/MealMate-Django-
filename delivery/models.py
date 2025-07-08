from django.db import models
from users.models import Customer

# Create your models here.
class Restaurant(models.Model):
    res_name = models.CharField(max_length=100)
    food_cat = models.CharField(max_length=200)
    rating = models.FloatField()
    img = models.URLField(default="https://www.citypng.com/public/uploads/preview/loading-load-icon-transparent-png-701751695033022vy5stltzj3.png")
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.res_name
    
class Menu(models.Model):
    res = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    category = models.CharField(max_length=50)
    item_img = models.URLField(default="https://www.citypng.com/public/uploads/preview/loading-load-icon-transparent-png-701751695033022vy5stltzj3.png")

    def __str__(self):
        return f"{self.item_name} - {self.res.res_name}"
    
    
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    items = models.ManyToManyField("Menu", through="CartItem")

    def total_price(self):
        return sum(item.item.price * item.quantity for item in self.cart_items.all())
    
    def __str__(self):
        return f"{self.customer.username} {self.total_price()}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cart_items')
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def item_total(self):
        return self.item.price * self.quantity
    
class Order(models.Model):
    razorpay_order_id = models.CharField(max_length=100, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.FloatField(null=True)
    items = models.ManyToManyField('Menu')
    order_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"