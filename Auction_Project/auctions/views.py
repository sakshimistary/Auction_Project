from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from auctions.serializers import AuctionSerializer, BidSerializer 
from rest_framework.permissions import IsAuthenticated 
from auctions.models import Auction, Bid
from django.utils import timezone
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


class PlaceBidView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BidSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            bid = serializer.save(user=request.user)

            auction = bid.auction
            auction.current_price = bid.amount
            auction.save()

            return JsonResponse({
                "message": "Bid placed successfully",
                "data": serializer.data
            }, status=201)

        return JsonResponse(serializer.errors, status=400)        
        
class AuctionBidsView(APIView):
    def get(self, request, auction_id):
        bids = Bid.objects.filter(auction_id=auction_id).order_by('-amount')
        serializer = BidSerializer(bids, many=True)

        return JsonResponse(serializer.data, safe=False, status=200)
    
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
            return "Winner declared successfully"
 
        return "No bids placed"  

class DeclareWinnerView(APIView):
    def post(self, request, auction_id):
        result = declare_winner(auction_id)
        return JsonResponse({"message": result})      