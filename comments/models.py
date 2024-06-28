from django.db import models
from django.contrib.auth.models import User
from studentswap.models import Item


# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    comment=models.CharField(default="")
    datecommented=models.DateTimeField(auto_now_add=True)
    # boolean value to check if item is in the wishlist or not
    is_wishlist=models.BooleanField(default=False)


