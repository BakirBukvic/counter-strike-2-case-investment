from django.shortcuts import render

# Create your views here.

from django.db.models import F, Sum, FloatField, ExpressionWrapper

def base(request):
    return render(request, 'base.html')


# generic case list view



def get_total_standing():
    from base.models import UserInventory
    qs = UserInventory.objects.select_related('case_bought')
    total = qs.annotate(
        diff=ExpressionWrapper(
            F('case_bought__price') - F('buy_price'),
            output_field=FloatField()
        ),
        total=ExpressionWrapper(
            (F('case_bought__price') - F('buy_price')) * F('ammount'),
            output_field=FloatField()
        )
    ).aggregate(sum_total=Sum('total'))['sum_total'] or 0
    return total