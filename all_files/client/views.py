from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from django.db.models import Q
from .forms import ClientForm
from django.urls import reverse_lazy



class ClientEditView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'
    success_url = reverse_lazy('client:list')

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'
    success_url = reverse_lazy('client:list')

    def get_object(self, queryset=None):
        return self.get_gueryset().get(pk=self.kwargs['pk'])


class clientListView(ListView):
    model = Client
    template_name = 'client/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )
        queryset = queryset.order_by('-created_at')
        return queryset