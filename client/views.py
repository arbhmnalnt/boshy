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
        queryset = super().get_queryset().order_by('-id')
        clinets_counter = len(queryset.all()) + 1
        for cl in queryset:
            if cl.counter == None or cl.counter == 0:
                print(f"order_counter before = > {clinets_counter}")
                clinets_counter -= 1
                cl.counter = clinets_counter
                print(f'client id => {cl.id} // client counter =>>>>>>>>>>>{cl.counter}')
                cl.save()
            else:
                pass
        search_query = self.request.GET.get('q')
        if search_query:
            # تحقق مما إذا كان البحث رقميًا أو نصيًا
            if search_query.isdigit():  # إذا كان رقميًا
                queryset = queryset.filter(
                    Q(counter=search_query)
                ).order_by('-id')
            else:  # إذا كان نصيًا
                queryset = queryset.filter(
                    Q(name__icontains=search_query)
                ).order_by('-id')

        return queryset