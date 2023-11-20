from django.urls import path
from.views import *

app_name = "client"

urlpatterns = [
    path('', clientListView.as_view(), name="client_list"),
    path('create/', ClientCreateView.as_view(), name='client_create'),

]