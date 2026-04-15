from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from auctions.serializers import AuctionSerializer, BidSerializer 
from rest_framework.permissions import IsAuthenticated 
from auctions.models import Auction
# Create your views here.

class CreateAuctionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AuctionSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return JsonResponse({"message": "Auction created successfully","data": serializer.data}, status=201)

        return JsonResponse(serializer.errors, status=400)
    
class AuctionListView(APIView):
    def get(self, request):
        is_active = request.data.GET.get('is_active')

        auctions = Auction.objects.all()

        if is_active is not None:
            auctions = auctions.filter(is_active = is_active)

        serializer = AuctionSerializer(auctions, many = True)

        return JsonResponse(serializer.data, safe=False)
        
class AuctionDetailView(APIView):
    def get(self, request, pk):
        try:
            auction = Auction.objects.get(pk = pk)

        except Auction.DoesNotExist:
            return JsonResponse({"error":"Auction not found"}, status = 404)
        
        serializer = AuctionSerializer(auction)

        return  JsonResponse(serializer.data, status =  200)
    
        
        
