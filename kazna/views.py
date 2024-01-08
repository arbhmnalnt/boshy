from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView 
from .models import *
from django.db.models import Q
# from .forms import *
from client.models import ClientSizes
from client.forms import ClientSizesForm
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
import json
from kazna.services import *
# Create your views here.
class recordsListView(ListView):
    model               =   Record
    template_name       =   'kazna/recordsList.html'
    context_object_name =   'records'
    ordering            =   '-created_at'