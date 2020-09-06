from django.db import models


class Game(models.Model):
    number = models.PositiveIntegerField(null=False, verbose_name='Загаданное число')
    status = models.BooleanField(verbose_name='Статус', default=False)
    amount = models.PositiveIntegerField(verbose_name='Количество попыток', default=0)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class Player(models.Model):
    games = models.ManyToManyField(Game, through='PlayerGameInfo', related_name='players')

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


class PlayerGameInfo(models.Model):
    creator = models.BooleanField(verbose_name='Игрок создатель', default=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Игрок')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Игра')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['player', 'game'], name='player_game'),
        ]