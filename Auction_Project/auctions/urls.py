from django.urls import path
from .views import CreateAuctionView, AuctionListView,AuctionDetailView,PlaceBidView,AuctionBidsView, DeclareWinnerView

urlpatterns = [
    path('create-auction/', CreateAuctionView.as_view()),
    path('auctions/', AuctionListView.as_view()),
    path('auction/<int:pk>/', AuctionDetailView.as_view()),
    path('place-bid/', PlaceBidView.as_view()),
    path('auction/<int:auction_id>/bids/', AuctionBidsView.as_view()),
    path('auction/<int:auction_id>/declare-winner/', DeclareWinnerView.as_view()),
]