from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
import requests
import json

from .models import Foods
from django.contrib.auth.models import User

PROPERTIES = [
    'code',
    'product_name',
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
            items = []
            for product in data['products']:
                item = {k: (product[k] if k in product else None)
                        for k in PROPERTIES}

                for k in item:
                    if not item[k]:
                        item[k] = "None"
                if item['categories_hierarchy'] != "None":
                    category = item['categories_hierarchy']
                    item['categories_hierarchy'] = category[-1][3:]
                items.append(item)
            context['products'] = sorted(
                items, key=lambda data: data['nutrition_grades'])
            context['status'] = 'ok'
            return context
        else:
            context['status'] = "no results"

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

    context = {}
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

    data = http_request(sub_payload)
    context = data
    context['selected'] = selected_item[0]

    return render(request, 'foods/subs.html', context)


@transaction.atomic()
def save(request):
    def check_db(item):
        name = item['product_name']
        code = item['code']
        image_url = item['image_small_url']

        product = Foods.objects.filter(code=code)

        if not product.exists():
            Foods.objects.create(
                code=code,
                name=name,
                image_url=image_url,

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

    return HttpResponse('ok')
