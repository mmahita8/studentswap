from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Item(models.Model):
    itemname=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    description=models.TextField()
    category=models.CharField(max_length=40)
    subcategory=models.CharField(max_length=40)
    imageurl=models.CharField(max_length=200)
    imagealt= models.CharField(max_length=200)
    date_posted=models.DateTimeField(auto_now_add=True)
    # boolean value to keep a track of the user's listings
    is_sold = models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.itemname

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])


# user login data
# regular_user={"username":"Mahita", "password": "regular"}
# admin_user={"username":"Admin", "password": "admin@23"}

