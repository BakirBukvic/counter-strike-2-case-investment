from django.urls import path
from .views import *

urlpatterns = [ 
    path('create/', create_case, name='create_case'),
    path ('', CaseListView.as_view(), name='case_list'),
    path('cases/delete/', delete_case_or_cases, name='delete_cases'),
    path('cases/edit-inline/<int:case_id>/', edit_case_inline, name='edit_case_inline'),

]