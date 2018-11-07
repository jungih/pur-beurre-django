from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from .models import Foods

import requests
import json
import copy
import re
from bs4 import BeautifulSoup

PROPERTIES = [
    'code',
    'product_name',
    'brands',
    'quantity',
    'image_url',
    'image_small_url',
    'categories_hierarchy',
    'nutrition_grades'

]


def http_request(payload):
    url = 'https://fr.openfoodfacts.org/cgi/search.pl'
    req = requests.get(url, params=payload)
    if req.status_code >= 200 and req.status_code <= 400:
        data = req.json()
        context = {}
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
                        if key == 'categories_hierarchy':
                            product[key] = item[key][-1][3:]
                        elif key == 'brands':
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

    # Search products
    if request.method == 'GET':
        query = request.GET.get('query')
        # API field for search query.
        product_payload = {
            'search_terms': query,
            'search_simple': 1,
            'json': 1,

        }

        # Get request
        context = http_request(product_payload)

        request.session['data'] = json.dumps(context)

    return render(request, 'foods/search.html', context)


def subs(request, category, code):

    products = request.session.get('data')
    products = json.loads(products)
    selected_item = [i for i in products['products'] if i['code'] == code]

    # API fields for searching products with A nutrition grade in the same category
    sub_payload = {
        'search_simple': 1,
        'action': 'process',
        'tagtype_0': 'categories',
        'tag_contains_0': 'contains',
        'tag_0': category,
        'nutriment_0': 'nutrition-score-fr',
        'nutriment_compare_0': 'lt',
        'nutriment_value_0': 11,
        'json': 1
    }
    # Get request for substitute products
    context = http_request(sub_payload)
    # Add item selected by user to context
    context['selected'] = selected_item[0]

    try:
        context['products'] = sorted(
            context['products'], key=lambda data: data['nutrition_grades'])
    except:
        pass
    return render(request, 'foods/subs.html', context)


def detail(request, code):

    req = requests.get(f'https://fr.openfoodfacts.org/product/{code}/').text

    def find_tag_from_string(string):

        try:
            soup = BeautifulSoup(req, 'lxml')
            tag = soup.find(text=re.compile(string))
            tag = tag.find_parent("div").contents
            tag.pop(1)
            return "".join([str(i) for i in tag])
        except:
            return 'Données non trouvées'

    score = find_tag_from_string("NutriScore")
    nutrient = find_tag_from_string("Repères")

    context = {
        'score': score,
        'nutrient': nutrient,
        'code': code
    }

    return render(request, 'foods/detail.html', context)


def mentions(request):
    return render(request, 'foods/mentions.html')


class FoodsDelete(DeleteView):
    model = Foods
    success_url = reverse_lazy('foods:myfoods')


@transaction.atomic()
def save(request):
    def check_db(item):
        name = item['product_name']
        code = item['code']
        image_url = item['image_small_url']
        grade = item['nutrition_grades']

        product = Foods.objects.filter(code=code)

        if not product.exists():
            Foods.objects.create(
                code=code,
                name=name,
                image_url=image_url,
                nutrition_grades=grade

            )

        return Foods.objects.get(code=item['code'])

    if request.method == 'POST':
        sub_data = json.loads(request.POST['sub'])
        product_data = json.loads(request.POST['product'])

        original = check_db(product_data)
        current_user = request.user
        original.author = current_user
        original.save()

        sub = check_db(sub_data)

        sub.substitute = original
        sub.save()

    return HttpResponse('Produit enregistré')


@login_required
def myfoods(request):
    user = request.user
    myfoods = user.foods_set.all().order_by('-created_at')

    context = {
        'myfoods': myfoods
    }
    return render(request, 'foods/myfoods.html', context)
