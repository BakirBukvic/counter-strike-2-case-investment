from .forms import CurrentCaseForm, UserInventoryForm
from base.models import CurrentCase, UserInventory
from django.views.generic import ListView
from django.db import IntegrityError
from django.shortcuts import render, redirect

from django.views.decorators.http import require_POST
import requests
import urllib.parse
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.urls import reverse

from django.utils import timezone
from datetime import date
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def update_all_case_prices_if_needed():
    today = date.today()
    cases = CurrentCase.objects.all()
    needs_update = cases.filter(last_price_update__date__lt=today).exists()
    if needs_update:
        for case in cases:
            new_price = fetch_steam_price(case.name)
            if new_price:
                case.price = new_price
                case.save()



def fetch_steam_price(item_name):
    encoded_name = urllib.parse.quote(item_name)
    url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={encoded_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            # Extract the lowest price, remove currency symbol, and convert to float
            lowest_price = data.get('lowest_price', '0').replace('$', '').replace(' USD', '').replace(',', '').strip()
            try:
                return float(lowest_price)
            except Exception:
                return 0.0
        else:
            return 0.0
    else:
        return 0.0


class InventoryListView(ListView):
    model = UserInventory
    template_name = 'user_inventory.html'
    context_object_name = 'inventory'

    def get_queryset(self):
        queryset = UserInventory.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(case_bought__name__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserInventoryForm()
        return context


class CaseListView(ListView):
    model = CurrentCase
    template_name = 'cases.html'
    context_object_name = 'cases'

    def get_queryset(self):
        # Update prices if needed before returning queryset
        update_all_case_prices_if_needed()
        queryset = CurrentCase.objects.all().order_by('name')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(hash_search__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CurrentCaseForm()
        return context

@csrf_exempt
@require_POST
def refresh_all_case_prices(request):
    try:
        from datetime import date
        today = date.today()
        cases = CurrentCase.objects.all()
        for case in cases:
            new_price = fetch_steam_price(case.name)
            if new_price:
                case.price = new_price
                case.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def edit_user_inventory(request, pk):
    try:
        data = json.loads(request.body)
        inventory_item = UserInventory.objects.get(pk=pk)
        # Update only the fields you expect from the frontend
        allowed_fields = ['case_bought', 'buy_price', 'ammount', 'buy_date']
        for field in allowed_fields:
            if field in data:
                setattr(inventory_item, field, data[field])
        inventory_item.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
def delete_user_inventory(request, pk):
    inventory_item = get_object_or_404(UserInventory, pk=pk)
    inventory_item.delete()
    return redirect('user_inventory')

@require_POST
def add_user_inventory(request):
    form = UserInventoryForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('user_inventory'))
    # If invalid, re-render the inventory list with errors
    inventory = UserInventory.objects.all()
    return render(request, 'user_inventory.html', {
        'form': form,
        'inventory': inventory,
    })



def create_case(request):
    error = None
    if request.method == 'POST':
        form = CurrentCaseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            hash_search = form.cleaned_data['hash_search']
            price = fetch_steam_price(name)  # Fetch price from Steam
            try:
                CurrentCase.objects.create(name=name, hash_search=hash_search, price=price)
                return redirect('case_list')
            except IntegrityError:
                error = "Name and hash search must be unique."
                cases = CurrentCase.objects.all().order_by('name')
                return render(request, 'cases.html', {
                    'form': form,
                    'cases': cases,
                    'error': error
                })
    return redirect('case_list')

@require_POST
def delete_case_or_cases(request):
    ids = request.POST.getlist('selected_cases')
    if ids:
        CurrentCase.objects.filter(id__in=ids).delete()
    return redirect('case_list')

from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
@csrf_exempt
def edit_case_inline(request, case_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            field = data.get('field')
            value = data.get('value')
            if field not in ['name', 'hash_search']:
                return JsonResponse({'success': False, 'error': 'Invalid field'})
            case = CurrentCase.objects.get(id=case_id)
            setattr(case, field, value)
            # If the name is updated, fetch the new price
            if field == 'name':
                case.price = fetch_steam_price(value)
            try:
                case.save()
            except IntegrityError:
                return JsonResponse({'success': False, 'error': f'{field.capitalize()} must be unique.'})
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


