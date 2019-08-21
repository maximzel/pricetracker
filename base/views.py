from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

from base.models import Rubric, Market, Product, Price
from base.tasks import update_db


def index(request):
    rubrics = Rubric.objects.all()
    markets = Market.objects.all()
    products = Product.objects.filter(available=True).order_by('name')
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_list = paginator.get_page(page)

    context = {
        'rubrics': rubrics,
        'markets': markets,
        'products_list': products_list,
    }
    return render(request, 'base/index.html', context)


def product(request, product_id):
    try:
        product_by_id = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    rubrics = Rubric.objects.all()
    markets = Market.objects.all()
    price_by_product = Price.objects.filter(product=product_id).order_by('-created')
    context = {
        'rubrics': rubrics,
        'markets': markets,
        'product_by_id': product_by_id,
        'price_by_product': price_by_product,
    }
    return render(request, 'base/product.html', context)


def rubric(request, rubric_id):
    try:
        rubric_by_id = Rubric.objects.get(pk=rubric_id)
    except Product.DoesNotExist:
        raise Http404("Rubric does not exist")
    rubrics = Rubric.objects.all()
    markets = Market.objects.all()
    products = Product.objects.filter(rubric=rubric_id).filter(available=True).order_by('name')
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_list = paginator.get_page(page)
    context = {
        'rubrics': rubrics,
        'markets': markets,
        'products_list': products_list,
        'rubric_by_id': rubric_by_id,
    }
    return render(request, 'base/index.html', context)


def market(request, market_id):
    try:
        market_by_id = Market.objects.get(pk=market_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    rubrics = Rubric.objects.all()
    markets = Market.objects.all()
    products = Product.objects.filter(market=market_id, available=True).order_by('name')
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_list = paginator.get_page(page)
    context = {
        'rubrics': rubrics,
        'markets': markets,
        'products_list': products_list,
        'market_by_id': market_by_id,
    }
    return render(request, 'base/index.html', context)


def search(request):
    query = request.GET.get('q')
    if query.startswith('http'):
        result = Product.objects.filter(original_url__search=query)
    else:
        result = Product.objects.filter(name__search=query)
    paginator = Paginator(result, 12)
    page = request.GET.get('page')
    products_list = paginator.get_page(page)
    rubrics = Rubric.objects.all()
    markets = Market.objects.all()
    context = {
        'rubrics': rubrics,
        'markets': markets,
        'products_list': products_list,
    }
    return render(request, 'base/index.html', context)


def update(request):
    update_db.delay()
    rubrics = Rubric.objects.all()
    markets = Market.objects.all()

    context = {
        'rubrics': rubrics,
        'markets': markets,
    }
    return render(request, 'base/done.html', context)
