from django.shortcuts import render, get_object_or_404, redirect, reverse, Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Game, Cart
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings


def home(request):
    return render(request, 'app/index.html', {
        'games': Game.objects.all(),
    })


class GamesListView(ListView):
    model = Game
    template_name = 'app/index.html'
    context_object_name = 'games'
    paginate_by = 9


class CartListView(ListView):
    model = Cart
    template_name = 'users/cart.html'
    context_object_name = 'cart'
    paginate_by = 9

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Cart.objects.filter(user=user)


class GameDetailView(DetailView):
    model = Game


class GameUpdateForm(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Game
    fields = ['title', 'genre', 'image_url', 'price', 'about']
    success_url = "/"
    extra_context = {'update': True}

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        if self.test_func():
            messages.success(self.request, 'Game Updated Successfully!')
            return super().form_valid(form)


@login_required
def add_to_cart(request, game_id):
    game = Game.objects.get(id=game_id)
    new_cart = Cart(user=request.user,
                    games=game)
    new_cart.save()
    messages.success(request, f"{game} has been added to you cart!")
    return redirect(reverse('cart', args=[request.user.username]))


@login_required
def delete_cart(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    cart.delete()
    messages.success(request, f"{cart} from cart deleted successfully!")
    return redirect(reverse('cart', args=[request.user.username]))


class GameDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Game
    success_url = "/"
    fields = '__all__'
    template_name = 'app/game_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        if self.test_func():
            messages.success(self.request, 'Game Deleted Successfully!')
            return super().form_valid(form)


class GameCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Game
    fields = '__all__'
    success_url = "/"

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        if self.test_func():
            messages.success(self.request, "Game Added Successfully")
            return super().form_valid(form)


@login_required
def create_checkout_session(request, game_id):
    game_buy = get_object_or_404(Cart, id=game_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": game_buy.games.title,
                                 "images": [game_buy.games.image_url]},
                "unit_amount": f"{int(game_buy.games.price)}00",
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f"your_host_url/success/{game_id}",
        cancel_url="your_host_url/cancel",
    )
    return redirect(checkout_session.url)


@login_required
def success(request, game_id):
    game_bought = get_object_or_404(Cart, id=game_id)
    game_bought.delete()
    return render(request, 'app/success.html', {
        'game': game_bought
    })


@login_required
def cancel(request):
    return render(request, 'app/cancel.html')


def search_games(request):
    if request.method == "POST":
        searched = request.POST['searched']
        games = Game.objects.filter(title__contains=searched)
        return render(request, 'app/search_games.html', {
            'searched': searched,
            'games': games,
        })
    else:
        raise Http404
