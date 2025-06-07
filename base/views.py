from django.shortcuts import render

# Create your views here.


def base(request):
    form = CurrentCaseForm()
   
    return render(request, 'base.html', {'form': form})


# generic case list view

