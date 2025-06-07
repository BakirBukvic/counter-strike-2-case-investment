from .forms import CurrentCaseForm
from base.models import CurrentCase
from django.views.generic import ListView
from django.db import IntegrityError
from django.shortcuts import render, redirect




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


def delete_case_or_cases(request, case_id=None):
    if case_id:
        try:
            case = CurrentCase.objects.get(id=case_id)
            case.delete()
        except CurrentCase.DoesNotExist:
            pass  # Handle the case where the case does not exist
    else:
        CurrentCase.objects.all().delete()  # Delete all cases if no specific case is provided
    return redirect('case_list')  # Redirect to the case list after deletion


def update_case_or_cases(request, case_id=None):
    if case_id:
        try:
            case = CurrentCase.objects.get(id=case_id)
            form = CurrentCaseForm(request.POST or None, instance=case)
            if form.is_valid():
                form.save()
                return redirect('case_list')
        except CurrentCase.DoesNotExist:
            pass  # Handle the case where the case does not exist
    else:
        # If no specific case is provided, just redirect to the case list
        return redirect('case_list')
    
    # Render the form for updating the case
    return render(request, 'update_case.html', {'form': form})