from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from django.db.models import Q
from .forms import *
from django.urls import reverse_lazy
from django.http import Http404



class ClothUpdateView(UpdateView):
    model = ClothRecord
    form_class = ClothRecordForm
    template_name = 'storge/cloth_form.html'
    success_url = reverse_lazy('cloth:list')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        cloth = Cloth.objects.get(pk=pk)
        clothRecord = ClothRecord.objects.create(clothh=cloth)   
        # cleanin 
        x = ClothRecord.objects.filter(clothh=cloth, amount__isnull=True)
        print(x.delete())
        return clothRecord 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        cloth = Cloth.objects.get(pk=pk)
        # Add your custom variable to the context
        context['historyRecords'] = ClothRecord.objects.filter(clothh=cloth, amount__gt=0)
        context['cloth'] = cloth
        return context
    
    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        cloth = Cloth.objects.get(pk=pk)

        cleaned_data = form.cleaned_data
        amount = cleaned_data["amount"]
        new_amount = amount + cloth.amount
        cloth.amount = new_amount
        cloth.save()
        
        response = super().form_valid(form)
        
        # Return the response
        return response
    
class ClothCreateView(CreateView):
    model = Cloth
    form_class = ClothForm
    template_name = 'storge/cloth_form.html'
    success_url = reverse_lazy('cloth:list')

class clothListView(ListView):
    model = Cloth
    template_name = 'storge/cloth_list.html'
    context_object_name = 'cloths'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )
        queryset = queryset.order_by('-created_at')
        return queryset