from django.urls import path
from .views import GamesListView, CartListView, GameDetailView, GameUpdateForm, GameCreateView
from . import views


urlpatterns = [
    path("", GamesListView.as_view(), name='e-home'),
    path('cart/<str:username>', CartListView.as_view(), name='cart'),
    path("game/<int:pk>/", GameDetailView.as_view(), name="game-detail"),
    path("game/<int:pk>/update/", GameUpdateForm.as_view(), name='game-update'),
    path('add-to-cart/<int:game_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete-cart/<int:cart_id>/', views.delete_cart, name='delete-cart'),
    path('delete-game/<int:pk>/', views.GameDeleteView.as_view(), name='game-delete'),
    path('game/new/', views.GameCreateView.as_view(), name='game-create'),
    path('create-checkout-session/<int:game_id>/', views.create_checkout_session, name='checkout-session'),
    path('success/<int:game_id>/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('search_games', views.search_games, name='search-games'),
]
