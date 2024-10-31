from django.urls import path
from.views import *

app_name = "img"

urlpatterns = [
    path('list/', imgListView.as_view(), name="list"),
    path('create/', imgCreateView.as_view(), name="create"),
    path('update/<int:pk>', imgUpdateView.as_view(), name="edit"),
    path('update_record/', byUserimgUpdateName, name="update_by_user"),
    path('delete/<int:pk>', imgDeleteView.as_view(), name="delete")
    
    # path('listOrderDetails/<int:pk>', ordersDetailView.as_view(), name="listOrderDetails")
]