from django.urls import path
from.views import *

app_name = "img"

urlpatterns = [
    path('list/', imgListView.as_view(), name="list"),
    path('create/', imgCreateView.as_view(), name="create")
    
    # path('listOrderDetails/<int:pk>', ordersDetailView.as_view(), name="listOrderDetails")
]