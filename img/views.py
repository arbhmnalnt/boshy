from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from django.db.models import Q
from .forms import *
from django.urls import reverse_lazy


class imgCreateView(CreateView):
    model = Img
    form_class = ImgForm
    template_name = 'img/img_form.html'
    success_url = reverse_lazy('img:list')
    def form_valid(self, form):
        response = super().form_valid(form)
        # Additional logic if needed
        return response


class imgListView(ListView):
    model               =   Img
    template_name       =   'img/img_list.html'
    context_object_name =   'imgs'

    def get_queryset(self):
        queryset        =   super().get_queryset()
        search_query    =   self.request.GET.get('q')

        if search_query : 
            queryset = queryset.filter(
                Q(name_icontains=search_query)|
                Q(id_eq=search_query)
            )
        queryset = queryset.order_by('-id')
        return queryset