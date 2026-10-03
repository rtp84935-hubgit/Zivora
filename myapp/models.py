from django.db import models
from django.contrib.auth.models import User
# Create your models here.

    
class seller(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    place=models.CharField(max_length=100) 
    LOGIN=models.OneToOneField(User,on_delete=models.CASCADE)
    
class customer(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    image=models.FileField()
    LOGIN=models.OneToOneField(User,on_delete=models.CASCADE)


class products(models.Model):
    SELLER=models.ForeignKey(seller,on_delete=models.CASCADE)
    ProductName = models.CharField(max_length=100)
    ProductPrice = models.IntegerField()
    ProductImage = models.FileField()
    ProductQuantity = models.CharField(max_length=100)
    ProductDescription = models.CharField(max_length=100)
    ProductStock = models.IntegerField()

class offer(models.Model):
    PRODUCT=models.ForeignKey(products,on_delete=models.CASCADE)
    offer=models.CharField(max_length=100)
    off=models.IntegerField()




class order(models.Model):
    USER=models.ForeignKey(customer,on_delete=models.CASCADE)
    orderDate=models.DateTimeField()
    amount=models.IntegerField()
    status=models.CharField(max_length=100,default='pending')

class orderDetails(models.Model):
    ORDER=models.ForeignKey(order,on_delete=models.CASCADE)
    PRODUCT=models.ForeignKey(products,on_delete=models.CASCADE)
    quantity=models.IntegerField()

class ReturnOrder(models.Model):
    ORDER_DETAILS=models.ForeignKey(orderDetails,on_delete=models.CASCADE)
    reason=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default='pending')


class cart(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    PRODUCT=models.ForeignKey(products,on_delete=models.CASCADE)
    date=models.DateTimeField()
    price=models.IntegerField()
    quantity=models.IntegerField()

class Feedback(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    PRODUCT=models.ForeignKey(products,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=10000)
    review=models.FloatField()
    type=models.CharField(max_length=100)

class used_product(models.Model):
    USER=models.ForeignKey(customer,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    product_image=models.FileField()
    product_price=models.IntegerField()
    product_description=models.CharField(max_length=100)

class UsedProductRequest(models.Model):
    USER=models.ForeignKey(customer,on_delete=models.CASCADE)
    DateTime=models.DateTimeField()
    UsedProduct=models.ForeignKey(used_product,on_delete=models.CASCADE)
    status=models.CharField(max_length=100,default='pending')
    


    





    


