from django.shortcuts import render

from .models import Player, Game, PlayerGameInfo
from .forms import GameForm
from django import http


def show_home(request):
    if not request.session.get('id_player'):
        player = Player.objects.create()
        id_player = player.id
        request.session['id_player'] = id_player
    else:
        id_player = request.session['id_player']
        player = Player.objects.get(id=id_player)

    form = GameForm()
    res = ''

    if not request.session.get('amount'):
        request.session['amount'] = 0
    if not request.session.get('creator'):
        request.session['creator'] = False

    game_last = Game.objects.last()
    if game_last is None:
        flag = False
    else:
        if not game_last.status:
            flag = False
        else:
            flag = True

    if not flag:
        game_begin = False

        if request.method == 'POST':
            data_form = GameForm(request.POST)
            if data_form.is_valid():
                game = Game.objects.create(number=data_form.data['number'], status=True)
                id_game = game.id
                PlayerGameInfo.objects.create(creator=True, player=player, game=game)
                request.session['id_game'] = id_game
                return http.HttpResponseRedirect('')
    else:
        game_begin = True
        game_last = Game.objects.last()
        id_game = game_last.id
        try:
            player_game_info = PlayerGameInfo.objects.get(player__id=id_player, game__id=id_game)
        except PlayerGameInfo.DoesNotExist:
            player_game_info = None
        if player_game_info is not None:
            if player_game_info.creator:
                request.session['creator'] = True
            else:
                if request.method == 'POST':
                    data_form = GameForm(request.POST)
                    if data_form.is_valid():
                        if not request.session.get('amount'):
                            request.session['amount'] = 0
                        request.session['amount'] += 1
                        game_last.amount = game_last.amount + 1
                        game_last.save()
                        if game_last.number == int(data_form.data['number']):
                            game_last.status = False
                            game_last.save()
                            return http.HttpResponseRedirect('')
                        else:
                            if game_last.number > int(data_form.data['number']):
                                res = f"Число > {data_form.data['number']}"
                            else:
                                res = f"Число < {data_form.data['number']}"
        else:
            request.session['creator'] = False
            PlayerGameInfo.objects.create(creator=False, player=player, game=game_last)
            request.session['id_game'] = id_game
            request.session['amount'] = 0

    context = {
        'form': form,
        'game_begin': game_begin,
        'creator': request.session['creator'],
        'game': game_last,
        'res': res,
        'amount': request.session['amount']
    }
    template = 'home.html'

    return render(request, template, context)