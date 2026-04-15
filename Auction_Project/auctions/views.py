from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from auctions.serializers import AuctionSerializer, BidSerializer 
from rest_framework.permissions import IsAuthenticated 
# Create your views here.

class CreateAuctionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AuctionSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return JsonResponse({"message": "Auction created successfully","data": serializer.data}, status=201)

        return JsonResponse(serializer.errors, status=400)
    

