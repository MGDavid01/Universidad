from django.shortcuts import render
from .forms import AnzueloMikeForm
from .models import AnzueloMike
#CreateViews
from django.views.generic.edit import CreateView

class Home(CreateView):
    model = AnzueloMike
    form_class = AnzueloMikeForm
    template_name = 'index.html'
    success_url = '/success/'  # Redirige a una URL de éxito después de guardar

def success_view(request):
    return render(request, 'succes.html', {'message': 'AnzueloMike creado exitosamente.'})