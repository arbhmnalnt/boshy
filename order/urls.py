from django.urls import path
from.views import *

app_name = "order"

urlpatterns = [
    # ========= START API  ==================
    path('payDebitRecord/<int:pk>/<int:paid>', payDebitRecord, name='payDebitRecord'),
    path('payDebit/<int:pk>', payDebit, name='payDebit'),
    path('changeOrderStatue/<int:pk>', chabgeOrderStatue),
    path('getClothStorgedAmount', getClothStorgedAmount),
    path('dublicate/<int:pk>', dublicate),
    path('delete_details/<int:pk>', DetailedOrderDelete, name='delete_details'),   # DetailedOrder   delete
    path('cleanup_orders/', cleanup_orders, name='cleanup_orders'),

    # ========= END API    ==================
    path('editDebit/<int:pk>', editDebitFormEditView.as_view(), name="editDebit"),
    path('listDebit/', debitListView.as_view(), name="listDebit"),
    path('createDeliverd/<int:pk>', DeliverdFormCreateView.as_view(), name="createDeliverd"),
    path('createMain', MasterInvoiceFormCreateView.as_view(), name="createMain"),
    path('createDetails/<int:pk>', DetailedOrderFormCreateView.as_view(), name="createDetails"),
    path('createBasicInfos/<int:pk>', BasicOrderFormCreateView.as_view(),name="finalPart"),
    path('list', ordersListView.as_view(), name="list"),
    path('daily_list', dailyOrdersListView.as_view(), name="daily_list"),

    path('listOrderDetails/<int:pk>', ordersDetailView.as_view(), name="listOrderDetails"),
    path('listorderStatus/', orderStatusListView.as_view(), name="orderStatus"),
    path('changeDetails/<int:order_id>/<int:masterInvoicePK>', change_details, name='changeDetails'),
    path('needToBeDoneOrders/', needToBeDoneOrders.as_view(), name="needToBeDoneOrders")
]