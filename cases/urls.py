from django.urls import path
from .views import *

urlpatterns = [ 
    path('create/', create_case, name='create_case'),
    path ('', CaseListView.as_view(), name='case_list'),
    path('cases/delete/', delete_case_or_cases, name='delete_cases'),
    path('cases/edit-inline/<int:case_id>/', edit_case_inline, name='edit_case_inline'),
    path('user-inventory/', InventoryListView.as_view(), name='user_inventory'),
    path('add-user-inventory/', add_user_inventory, name='add_user_inventory'),
        path('inventory/edit/<int:pk>/', edit_user_inventory, name='edit_user_inventory'),
    path('inventory/delete/<int:pk>/', delete_user_inventory, name='delete_user_inventory'),
    path('refresh-all-case-prices/', refresh_all_case_prices, name='refresh_all_case_prices'),
]