from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Foods

import requests
import json
import copy
import re
from bs4 import BeautifulSoup

PROPERTIES = [
    'code',
    'product_name_fr',
    'brands',
    'quantity',
    'image_url',
    'categories_hierarchy',
    'nutrition_grades',


]


def http_request(payload):
    url = 'https://fr.openfoodfacts.org/cgi/search.pl'
    req = requests.get(url, params=payload)
    context = {}
    if req.ok:
        data = req.json()
        if data['count'] > 0:

            products = []
            for item in data['products']:
                product = {}
                for key in PROPERTIES:

                    try:
                        if not item[key]:
                            raise KeyError
                    except KeyError:
                        product[key] = "None"
                    else:
                        if key == 'brands':
                            product[key] = item[key].split(',')[-1]
                        else:
                            product[key] = item[key]

                products.append(product)

                # item = (k: v if v else "None"
                #         for k, v in {k: product[k] if k in product else None
                #             for k in PROPERTIES}.items())
            context['products'] = products

            context['status'] = 'ok'
            return context
        else:
            context['status'] = "Aucun produit n'a été trouvé."
            return context
    else:
        context['status'] = f'Error: {req.status_code}'
        return context


def index(request):
    return render(request, 'foods/index.html')


def search(request):

    context = {}
    # Search products
    if request.method == 'GET':
        query = request.GET.get('query')
        # search products from DB
        if query:
            products_list = Foods.objects.filter(
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

    # search substitutes from foods
    # get a querySet and loop thorugh categories

    context = {'status': "Aucun produit n'a été trouvé."}

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


class FoodsDelete(DeleteView):
    model = Foods
    success_url = reverse_lazy('foods:myfoods')


@transaction.atomic()
def save(request):
    current_user = request.user

    def add_db(item):
        food = Foods.objects.create(
            code=item['code'],
            name=item['product_name_fr'],
            image_url=item['image_small_url'],
            nutrition_grades=item['nutrition_grades'],
            brands=item['brands'],
            quantity=item['quantity'])
        return food

    if request.method == 'POST':
        sub_data = json.loads(request.POST['sub'])
        product_data = json.loads(request.POST['product'])
        try:
            with transaction.atomic():
                product = Foods.objects.filter(
                    author=current_user, code=product_data['code'])

                if not product.exists():
                    original = add_db(product_data)
                else:
                    original = product.first()
                original.author = current_user
                original.save()
                sub = add_db(sub_data)
                sub.substitute = original
                sub.save()
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
