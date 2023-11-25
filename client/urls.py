from django.urls import path
from.views import *

app_name = "client"

urlpatterns = [
    path('', clientListView.as_view(), name="list"),
    path('create/', ClientCreateView.as_view(), name='create'),
    path('edit/<int:pk>', ClientEditView.as_view(), name='edit'),

]