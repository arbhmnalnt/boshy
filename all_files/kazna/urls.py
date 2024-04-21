from django.urls import path
from.views import *

app_name = "kazna"

urlpatterns = [
    path('list/', recordsListView.as_view(), name="list"),
    path('pay/<int:pk>/<int:paid>', pay),
    # path('createDetails/<int:pk>', DetailedOrderFormCreateView.as_view(), name="createDetails"),
    # path('createBasicInfos/<int:pk>', BasicOrderFormCreateView.as_view(),name="finalPart"),
    
    # path('listOrderDetails/<int:pk>', ordersDetailView.as_view(), name="listOrderDetails")
]