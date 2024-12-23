from django.db import models
from django.contrib.auth.models import User

class Product(models.Model): #not using
    name= models.CharField(max_length=100)
    price =models.IntegerField()
    pdetails=models.CharField(max_length=100)
    cat=models.IntegerField()
    # brand=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)

class Products(models.Model):
    CAT=((1,'dairy'),(2,'fruits'),(3,'vegetables'),(4,'Pasta_rice_cereals'),(5,'Meat_alternatives'),(6,'Cans_jars'),(7,'Bread_baked'),(8,'Frozen_food'),(9,'sauces'),(10,'Nuts_snacks'),(11,'beverages'),(12,'herbs_spices'))
    name= models.CharField(max_length=100,verbose_name='Product Name')
    price =models.IntegerField()
    pdetails=models.CharField(max_length=100,verbose_name='Product Details')
    cat=models.IntegerField(choices=CAT,verbose_name='Categgory')
    brand=models.CharField(max_length=100, verbose_name='Brand')
    is_active=models.BooleanField(default=True, verbose_name='Availabel')
    # image upload in table
    pimage=models.ImageField(upload_to='image')

class Cart(models.Model):
    uid=models.ForeignKey(User, on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Products, on_delete=models.CASCADE,db_column='pid')
    # tpid=models.ForeignKey(Top_Products, on_delete=models.CASCADE,db_column='tpid')
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User, on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Products, on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
