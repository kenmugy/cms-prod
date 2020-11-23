from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True)
    name = models.CharField( max_length=200, null=True)
    phone = models.CharField( max_length=200, null=True)
    date_created = models.DateTimeField( auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Customer_detail", kwargs={"pk": self.pk})

class Item(models.Model):
    item_no = models.CharField("Item name",max_length=50, null=True)
    # size = models.CharField( max_length=50, null=True)
    # color = models.CharField( max_length=50, null=True)
    quantity = models.IntegerField(default = 0, null=True)
    date_created = models.DateTimeField( auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.item_no}"

    def get_absolute_url(self):
        return reverse("Item_detail", kwargs={"pk": self.pk})

class Order(models.Model):
    STATUSES = (
        ("Delivered", "Delivered"),
        ("Pending", "Pending"),
        # ("Out for Delivery", "Out for Delivery"),
    )
    name = models.CharField("Item", max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null= True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null= True)
    quantity = models.IntegerField(default = 0, null = True)
    status = models.CharField( max_length=200, choices = STATUSES,default="Pending", null=True)
    date_created = models.DateTimeField( auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"no.{self.id} | status {self.status}"

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

# class OrderHistory(models.Model):
#     STATUSES = (
#         ("Delivered", "Delivered"),
#         ("Pending", "Pending"),
#         # ("Out for Delivery", "Out for Delivery"),
#     )
#     name = models.CharField("Item", max_length=50)
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null= True)
#     item = models.ForeignKey(Item, on_delete=models.SET_NULL, null= True)
#     quantity = models.IntegerField(default = 0, null = True)
#     status = models.CharField( max_length=200, choices = STATUSES,default="Pending", null=True)
#     date_created = models.DateTimeField( auto_now=False, auto_now_add=True)

#     def __str__(self):
#         return f"no.{self.id} | status {self.status}"

    # def get_absolute_url(self):
    #     return reverse("Order_detail", kwargs={"pk": self.pk})