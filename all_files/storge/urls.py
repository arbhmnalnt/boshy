from django.urls import path
from.views import *

app_name = "cloth"

urlpatterns = [
    path('', clothListView.as_view(), name="list"),
    path('create/', ClothCreateView.as_view(), name='create'),
    path('edit/<int:pk>', ClothUpdateView.as_view(), name='edit'),

]