from django.forms import ModelForm, HiddenInput
from .models import AnzueloMike

class AnzueloMikeForm(ModelForm):
    class Meta:
        model = AnzueloMike
        fields = '__all__'

        widgets = {
            'latitud': HiddenInput(),
            'longitud': HiddenInput(),
        }