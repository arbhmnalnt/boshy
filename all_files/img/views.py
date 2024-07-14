from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from django.db.models import Q
from .forms import *
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import Http404, HttpResponseRedirect, JsonResponse



@csrf_exempt
def byUserimgUpdateName(request):
    if request.method == "POST":
        data                    = json.loads(request.body.decode('utf-8'))
        old_img_name                   = data.get('activatedImgId')
        new_image_name                = data.get('newImgName')
        Img.objects.filter(name=old_img_name).update(name=new_image_name)

        response_data = {
            'status': 'success',
        }

    return JsonResponse(response_data)



class imgDeleteView(DeleteView):
    model           =   Img
    # form_class      =   ImgForm
    template_name   =   'img/img_confirm_delete.html'
    success_url = reverse_lazy('img:list')


class imgUpdateView(UpdateView):
    model           =   Img
    form_class      =   ImgForm
    template_name   =   'img/img_form.html'
    success_url = reverse_lazy('img:list')

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
        if str(search_query) == "NoneType":
            try:
                # Try to filter by ID if the search query is a valid integer
                id_query = Q(id__exact=int(search_query))
            except ValueError:
                # If not a valid integer, exclude the ID filter
                id_query = Q()

            queryset = queryset.filter(
                Q(name__icontains=search_query) | id_query
            )
        queryset = queryset.order_by('-id')
        return queryset