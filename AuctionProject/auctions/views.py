from django.shortcuts import render
from rest_framework import viewsets
from auctions.models import Auction, Bid
from auctions.serializers import AuctionSerializer, BidSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
class AuctionView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        auctions = Auction.objects.filter(is_active = True)

        serializer = AuctionSerializer(auctions, many = True)

        print(timezone.now())
        return Response(serializer.data)
        
    def create(self, request):

        serializer = AuctionSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save(owner = request.user)
            return Response({'message' : "Auction created Successfully!!"})
        
        return Response(serializer.errors)

    def retrieve(self, request, pk):
        
        try:
            data = Auction.objects.get(id = pk)
            serializer = AuctionSerializer(data)
            return Response(serializer.data)
        
        except Auction.DoesNotExist:
            return Response({'message':'Auction Not found!!'})
        

        
class PLaceBidViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        serializer = BidSerializer(data = request.data , context = {'request': request} ) 
        if serializer.is_valid():
            bid = serializer.save(user = request.user)
            auction = bid.auction 
            auction.current_price = bid.amount  
            auction.save()

            return Response({'message':'Bid placed Successfully!!'})   

        return Response(serializer.errors)
    
    def retrieve(self, request, pk):
        try:
            bids = Bid.objects.filter(auction_id = pk).order_by('-amount')
            serializer = BidSerializer(bids, many = True)
            return Response(serializer.data)
        
        except Auction.DoesNotExist:
            return Response({"message": "Auction not Found!!"})
        
    def destroy(self, request, pk):
        bid = Bid.objects.get(id = pk)
        bid.delete()    
        
def declare_winner(auction_id):
    try:
        auction = Auction.objects.get(id=auction_id)
    except Auction.DoesNotExist:
        return "Auction not found"
    
    if auction.end_time > timezone.now():
        return "Auction still ongoing"

    else:
        highest_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()

        if highest_bid:
            auction.winner = highest_bid.user
            auction.is_active = False
            auction.save()
            return f'{auction.winner} is the winner!!'
 
        return "No bids placed"          
    
class WinnerViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk):
        winner = declare_winner(auction_id = pk)
        
        return Response({'message': winner})
        