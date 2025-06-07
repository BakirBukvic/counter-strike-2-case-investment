from django.urls import path
from .views import *

urlpatterns = [ 
    path('create/', create_case, name='create_case'),
    path ('', CaseListView.as_view(), name='case_list'),
]