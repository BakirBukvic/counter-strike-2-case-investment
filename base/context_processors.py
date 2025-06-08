from .views import get_total_standing

def total_standing(request):
    total = get_total_standing()
    return {'total_standing': total}