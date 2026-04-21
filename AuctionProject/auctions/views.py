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

