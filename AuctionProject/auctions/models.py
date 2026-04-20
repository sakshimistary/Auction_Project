from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Auction(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()

    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")

    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="bids", null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
    
    