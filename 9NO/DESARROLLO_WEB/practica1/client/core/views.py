from django.shortcuts import redirect, render
from django.views import generic
import requests

API_BASE = "http://127.0.0.1:8000"


class ListBank(generic.View):
    template_name = "core/list_bank.html"
    url_base = f"{API_BASE}/v1/banks/list/"

    def get(self, request):
        response = requests.get(url=self.url_base)
        context = {"banks": response.json()}
        return render(request, self.template_name, context)


class CreateBank(generic.View):
    template_name = "core/create_bank.html"
    url_base = f"{API_BASE}/v1/bank/create/"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        payload = {
            "name": request.POST.get("name"),
            "address": request.POST.get("address"),
        }
        requests.post(url=self.url_base, json=payload)
        return redirect("core:list_bank")


class DetailBank(generic.View):
    template_name = "core/detail_bank.html"
    url_base = f"{API_BASE}/v1/bank/detail/"

    def get(self, request, pk):
        response = requests.get(url=f"{self.url_base}{pk}/")
        context = {"bank": response.json()}
        return render(request, self.template_name, context)


class UpdateBank(generic.View):
    template_name = "core/update_bank.html"
    url_detail = f"{API_BASE}/v1/bank/detail/"
    url_base = f"{API_BASE}/v1/bank/update/"

    def get(self, request, pk):
        response = requests.get(url=f"{self.url_detail}{pk}/")
        context = {"bank": response.json()}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        payload = {
            "name": request.POST.get("name"),
            "address": request.POST.get("address"),
            "status": request.POST.get("status") == "on",
        }
        requests.put(url=f"{self.url_base}{pk}/", json=payload)
        return redirect("core:list_bank")


class DeleteBank(generic.View):
    template_name = "core/delete_bank.html"
    url_detail = f"{API_BASE}/v1/bank/detail/"
    url_base = f"{API_BASE}/v1/bank/delete/"

    def get(self, request, pk):
        response = requests.get(url=f"{self.url_detail}{pk}/")
        context = {"bank": response.json()}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        requests.delete(url=f"{self.url_base}{pk}/")
        return redirect("core:list_bank")
