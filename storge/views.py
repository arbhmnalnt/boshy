from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from django.db.models import Q
from .forms import *
from django.urls import reverse_lazy


class ClothUpdateView(UpdateView):
    model = ClothRecord
    form_class = ClothRecordForm
    template_name = 'storge/cloth_form.html'
    success_url = reverse_lazy('cloth:list')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Cloth.objects.get(pk=pk)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'clothh': self.kwargs.get('pk')}
        return kwargs

    def form_valid(self, form):
        # Create a new ClothRecord
        cloth_record = form.save(commit=False)
        # Update the related Cloth with the new amount
        cloth                   = Cloth.objects.get(pk=self.kwargs.get('pk'))
        form_amount             = form.cleaned_data['amount']
        previous_cloth_amount   = cloth.amount 
        total_amount            = int(previous_cloth_amount) + int(form_amount)
        form.cleaned_data['amount']            = total_amount

        print(f'{previous_cloth_amount} / {form_amount}  / {total_amount}  {type(cloth.amount)} = {type(total_amount)}')
        cloth.save()
        # Save the ClothRecord
        cloth_record.save()

        #ClothRecord
        newClothRecord   = ClothRecord.objects.create(
            clothh   =  cloth,
            amount  =  form_amount,
            typee   = "inside"
        )
        return super().form_valid(form)
    
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