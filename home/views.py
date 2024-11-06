from django.shortcuts import render
from datetime import date
from order.models import basicInvoiceInfo

# Create your views here.

def index(request):
    # Get the urgent orders
    urgenO = urgenOrders()
    # Get the overtime orders
    overTimeOrdersList = overTimeOrders()

    # Pass both sets of orders to the template
    ctx = {
        'overTimeOrders': overTimeOrdersList,
        'urgentOrders': urgenO,
    }

    return render(request, 'homee/homepage.html', context=ctx)


def overTimeOrders(today_date=None):
    if not today_date:
        today_date = date.today()

    overdue_orders_datails = basicInvoiceInfo.objects.filter(
        receve_date__lt=today_date,
        statue__in=["unknwon", "sent", "returned", "doneAgain", "urgent"]
    )  # Exclude "done" and "delivered"

    overdue_orders = [
        {
            'master_invoice': order.masterInvoice,
            'statue': order.statue_display  # Add the status to the dictionary
        }
        for order in overdue_orders_datails
    ]
    return overdue_orders


def urgenOrders(today_date=None):
    if not today_date:
        today_date = date.today()

    urgent_orders_datails = basicInvoiceInfo.objects.filter(
        statue__in=["urgent"]
    )  # Filter for "urgent" orders

    urgent_orders = [
        {
            'master_invoice': order.masterInvoice,
            'last_modified_date': order.updated_at  # Add the status to the dictionary
        }
        for order in urgent_orders_datails
    ]
    return urgent_orders
