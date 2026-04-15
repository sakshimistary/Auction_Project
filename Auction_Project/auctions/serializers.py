from rest_framework import serializers
from auctions.models import Auction,Bid
from django.utils import timezone

class AuctionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source= 'owner.username')

    class Meta:
        model = Auction
        fields = "__all__"
        read_only_fields = ['current_price', 'is_active', 'created_at']

    def validate_end_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("End time must be in the future")
        return value
        

class BidSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Bid
        fields = "__all__"
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        auction = data.get('auction')
        amount = data.get('amount')
        
        if not auction.is_active:
            raise serializers.ValidationError("Auction is not active")
        
        if auction.end_time <= timezone.now():
            raise serializers.ValidationError("Auction has ended")

        if amount <= auction.current_price:
            raise serializers.ValidationError(f"Bid must be greater than current price ({auction.current_price})")
        
        if auction.owner == self.context['request'].user:
            raise serializers.ValidationError("You cannot bid on your own auction")
        
        return data
    