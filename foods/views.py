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
            paginator = Paginator(products_list, 6)  # Show 6 products perpage
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
    if not context['status']:
        context['status'] = "Aucun produit n'a été trouvé."

    return render(request, 'foods/subs.html', context)


class Scrap:
    """Scrap html code from openfoodfacts.org using
    BeutifulSoup4
    """

    def __init__(self, code):
        req = requests.get(
            f'https://fr.openfoodfacts.org/product/{code}/').text
        self.soup = BeautifulSoup(req, 'lxml')

    def get_div(self, string):
        self.string = string

        try:
            tag = self.soup.find(string=re.compile(self.string))
            tag = tag.find_parent("div").contents
            tag.pop(1)
            return "".join([str(i) for i in tag])
        except:
            return 'Les données non présentes'

    def get_img(self, string):
        self.string = string
        try:
            tag = self.soup.find('img', class_=self.string)
            image = tag['data-src']
            return image
        except:
            return None

    def get_name(self):
        try:
            tag = self.soup.find('h1')
            name = tag.string
            return name
        except:
            return None


def detail(request, code):
    s = Scrap(code)
    score = s.get_div("NutriScore")
    nutrient = s.get_div("Repères")
    image_url = s.get_img("show-for-xlarge-up")
    name = s.get_name()
    context = {
        'score': score,
        'nutrient': nutrient,
        'code': code,
        'image_url': image_url,
        'name': name
    }

    return render(request, 'foods/detail.html', context)


def mentions(request):
    return render(request, 'foods/mentions.html')


def delete(request, id, sub_id):
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


@transaction.atomic()
def save(request):
    current_user = request.user

    if request.method == 'POST':
        selected_pk = json.loads(request.POST['selected'])
        sub_pk = json.loads(request.POST['sub'])
        try:
            with transaction.atomic():
                selected_product = Food.objects.get(pk=selected_pk)
                selected_product.author.add(current_user)
                selected_product.save()

                sub_product = Food.objects.get(pk=sub_pk)
                sub_product.substitute.add(selected_product)
                sub_product.save()

            return HttpResponse(status=201)
        except IntegrityError:
            return HttpResponse(status=409)


@login_required
def myfoods(request):
    user = request.user
    myfoods = user.foods_set.all().order_by('-created_at')

    context = {
        'myfoods': myfoods
    }
    return render(request, 'foods/myfoods.html', context)
