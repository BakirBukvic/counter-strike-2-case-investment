from .forms import CurrentCaseForm
from base.models import CurrentCase
from django.views.generic import ListView
from django.db import IntegrityError
from django.shortcuts import render, redirect

from django.views.decorators.http import require_POST



class CaseListView(ListView):
    model = CurrentCase
    template_name = 'cases.html'
    context_object_name = 'cases'

    def get_queryset(self):
        return CurrentCase.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CurrentCaseForm()
        return context


def create_case(request):
    error = None
    if request.method == 'POST':
        form = CurrentCaseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            hash_search = form.cleaned_data['hash_search']
            price = 10.00  # Mimic API call
            try:
                CurrentCase.objects.create(name=name, hash_search=hash_search, price=price)
                return redirect('case_list')
            except IntegrityError:
                error = "Name and hash search must be unique."
                # Show the cases page with the error
                cases = CurrentCase.objects.all().order_by('name')
                return render(request, 'cases.html', {
                    'form': form,
                    'cases': cases,
                    'error': error
                })
    # For GET or any other case, just redirect to the cases list
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

@csrf_exempt
def edit_case_inline(request, case_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            case = CurrentCase.objects.get(id=case_id)
            if 'name' in data:
                case.name = data['name']
            if 'price' in data:
                case.price = data['price']
            if 'hash_search' in data:
                case.hash_search = data['hash_search']
            case.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})