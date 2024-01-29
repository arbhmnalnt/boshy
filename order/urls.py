from django.urls import path
from.views import *

app_name = "order"

urlpatterns = [
    # ========= API
    path('changeOrderStatue/<int:pk>', chabgeOrderStatue),
    path('getClothStorgedAmount', getClothStorgedAmount),
    # ========= API

    path('createMain', MasterInvoiceFormCreateView.as_view(), name="createMain"),
    path('createDetails/<int:pk>', DetailedOrderFormCreateView.as_view(), name="createDetails"),
    path('createBasicInfos/<int:pk>', BasicOrderFormCreateView.as_view(),name="finalPart"),
    path('list', ordersListView.as_view(), name="list"),
    path('listOrderDetails/<int:pk>', ordersDetailView.as_view(), name="listOrderDetails")
]