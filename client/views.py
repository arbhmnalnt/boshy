from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from django.db.models import Q
from .forms import ClientForm
from django.urls import reverse_lazy
from django.contrib import messages



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

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValueError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )
        queryset = queryset.order_by('-created_at')
        return queryset