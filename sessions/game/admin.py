from django.contrib import admin
from .models import PlayerGameInfo, Game, Player


class PlayerGameInfoInline(admin.TabularInline):
    model = PlayerGameInfo
    extra = 0


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = (PlayerGameInfoInline,)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):

    pass