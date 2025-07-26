from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null= True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Đơn hàng #{self.pk} - {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)