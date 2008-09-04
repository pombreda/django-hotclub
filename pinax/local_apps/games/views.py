from arcade.models import Game, ArcadeCategory

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

def game_list(request, sort="most-played", category=None):
    cats = ArcadeCategory.objects.all()
    cats = [(c, c.game_set.filter(downloaded=True).count()) for c in cats]
    games = Game.objects.filter(downloaded=True)
    if category is not None:
        category = get_object_or_404(ArcadeCategory, slug=category.lower())
        games = category.game_set.filter(downloaded=True)
    if sort == 'most-played':
        games = games.order_by('-game_plays')
    elif sort == 'alphabetical':
        games = games.order_by('name')
    elif sort == 'newest':
        games = games.order_by('-created')
    context = {
        'games': games,
        'sort': sort,
        'category': category,
        'categories': cats,
    }
    return render_to_response('games/game_list.html',
        context, context_instance=RequestContext(request))

def categories(request):
    cats = ArcadeCategory.objects.all()
    cats = [(c, c.game_set.filter(downloaded=True).count()) for c in cats]
    context = {
        'categories': cats,
    }
    return render_to_response('games/category_list.html',
        context, context_instance=RequestContext(request))

def game_detail(request, slug=''):
    game = get_object_or_404(Game, slug=slug.lower())
    if request.META.get('HTTP_REFERER', '') != request.path:
        game.add_play()
    context = {
        'game': game,
    }
    return render_to_response('games/game_detail.html',
        context, context_instance=RequestContext(request))