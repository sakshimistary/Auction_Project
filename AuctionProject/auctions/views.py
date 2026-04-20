from django.shortcuts import render
from rest_framework import viewsets
from auctions.models import Auction, Bid
from auctions.serializers import AuctionSerializer, BidSerializer
from rest_framework.response import Response

class AuctionView(viewsets.ViewSet):
    def list(self, request):
        auctions = Auction.filter(is_active = "is_active")

        serializer = AuctionSerializer(auctions, many = True)

        return Response(serializer.data)

