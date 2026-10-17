from django.shortcuts import render
from django.views import generic
import requests

# Create your views here.

class ListBank(generic.View):
    template_name = "core/list_bank.html"
    context = {}
    response = {}
    url_base = ""
    banks = None

    def get(self, request):
        self.response = requests.get(url=self.url_base).json()
        self.context = {
            "banks": self.response
        }
        return render(request, self.template_name, self.context)
    