from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Food

import requests
import json
import copy
import re
from bs4 import BeautifulSoup


def index(request):
    return render(request, 'foods/index.html')


def search(request):

    context = {}
    # Search products
    if request.method == 'GET':
        query = request.GET.get('query')
        # search products from DB
        if query:
            products_list = Food.objects.filter(
                product_name__icontains=query).order_by('id')
            if products_list:
                # Show 6 products perpage
                paginator = Paginator(products_list, 6)
                page = request.GET.get('page')
                products = paginator.get_page(page)
                context['products'] = products
                context['query'] = query
                context['status'] = 'ok'
            else:
                context['status'] = "Aucun produit n'a été trouvé."

    return render(request, 'foods/search.html', context)


def subs(request, code):
    context = {}
    # search substitutes from foods
    selected = Food.objects.get(code=code)
    # get a querySet and loop thorugh categories
    context['selected'] = selected

    categories = selected.categories_fr.split(',')

    for category in reversed(categories):
        subs_list = Food.objects.filter(
            Q(categories_fr__icontains=category) &
            Q(nutrition_grade_fr__lt='c')
        ).exclude(id=selected.id).order_by('nutrition_grade_fr', 'id')
        paginator = Paginator(subs_list, 6)
        page = request.GET.get('page')
        subs = paginator.get_page(page)
        if subs:
            context['status'] = 'ok'
            context['subs'] = subs
            break
    if 'status' not in context:
        context['status'] = "Aucun produit n'a été trouvé."

    return render(request, 'foods/subs.html', context)


def detail(request, code):

    product = Food.objects.get(code=code)
    image_score = f'foods/img/nutriscore-{product.nutrition_grade_fr}.svg'

    context = {
        'product': product,
        'image_score': image_score
    }

    return render(request, 'foods/detail.html', context)


def mentions(request):
    return render(request, 'foods/mentions.html')


@transaction.atomic()
def save(request):
    current_user = request.user

    if request.method == 'POST':
        selected_pk = json.loads(request.POST['selected'])
        sub_pk = json.loads(request.POST['sub'])
        try:
            with transaction.atomic():
                selected_product = Food.objects.get(pk=selected_pk)
                if current_user not in selected_product.author.all():
                    selected_product.author.add(current_user)
                    selected_product.save()

                sub_product = Food.objects.get(pk=sub_pk)
                if sub_product not in selected_product.substitute.all():
                    sub_product.substitute.add(selected_product)
                    sub_product.save()

            return HttpResponse(status=201)
        except IntegrityError:
            return HttpResponse(status=409)


@login_required
def myfoods(request):
    user = request.user
    myfoods = user.food_set.all().order_by('id')

    context = {
        'myfoods': myfoods
    }
    return render(request, 'foods/myfoods.html', context)


def delete(request, id, sub_id):
    """Removes relation"""

    obj = get_object_or_404(Food, id=id)

    if sub_id:
        sub = get_object_or_404(Food, id=sub_id)
    else:
        sub = None
    context = {
        'selected': obj,
        'sub': sub
    }

    if request.method == 'POST':
        if not sub:
            obj.author.remove(request.user)
            obj.substitute.clear()
            obj.save()
        else:
            obj.substitute.remove(sub)
            obj.save()
        return redirect('foods:myfoods')
    return render(request, 'foods/foods_confirm_delete.html', context)
