from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import generic
from .models import Player, Game
from .forms import SignUpForm, LoginForm, CreateGameForm, ManageProfileForm

def index(request):
    return render(request, 'futeboladas/index.html', {'user': request.user})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('futeboladas:index')

    next = ""
    if request.GET:
        next = request.GET['next']

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)

            # redirect to correct page if there is a next arg
            if next == "":
                return redirect('futeboladas:index')
            else:
                return redirect(next)
    else:
        form = LoginForm()
    return render(request, 'futeboladas/login.html', {'form': form})

def logout_view(request):
    # TODO if no user is currently logged in, display message saying that
    logout(request)
    return redirect('futeboladas:index')

def signup(request):
    if request.user.is_authenticated:
        return redirect('futeboladas:index')
        
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('futeboladas:index')
    else:
        form = SignUpForm()
    return render(request, 'futeboladas/signup.html', {'form': form})

@login_required
def manage_profile(request):
    if request.method == 'POST':
        form = ManageProfileForm(request.POST, user=request.user)
        if form.is_valid():
            update_session_auth_hash(request, form.user)
            return redirect('futeboladas:profile')
    else:
        form = ManageProfileForm()
    return render(request, 'futeboladas/manage_profile.html', {'form': form})

@login_required
def create_game(request):
    if request.method == 'POST':
        form = CreateGameForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('futeboladas:game_detail', pk=form.pk)
    else:
        form = CreateGameForm()
    return render(request, 'futeboladas/create_game.html', {'form': form})

class GamesListView(generic.ListView):
    model = Game
    template_name = "futeboladas/games.html"
    context_object_name = 'games'

    def get_queryset(self):
        """
        Excludes any games that aren't administered by the logged in user.
        """
        user = self.request.user
        # Get player's games list
        player = Player.objects.get(user_id=user.id)

        games_dictionary = {}

        games_dictionary['administered'] = Game.objects.filter(admin=player.id)
        games_dictionary['invited'] = Game.objects.filter(players=player)
        games_dictionary['public'] = Game.objects.filter(private=False)

        return games_dictionary

@login_required
def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    player = Player.objects.get(user_id=request.user.id)
    authorized = (player in game.players.all()) or (player == game.admin) or not game.private

    return render(request, 'futeboladas/game_detail.html', {'game': game, 'authorized': authorized})

def friends(request):
    return HttpResponse("Friends Info Page")

class ProfileView(generic.DetailView):
    model = User
    template_name = 'futeboladas/profile.html'
    context_object_name = 'authenticated_user'