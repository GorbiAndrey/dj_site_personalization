from django import forms
from .models import Game


class GameForm(forms.ModelForm):
    number = forms.IntegerField(min_value=1, max_value=10, label='Число')

    class Meta(object):
        model = Game
        exclude = ('id', 'status', 'amount', )