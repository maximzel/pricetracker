import requests
from django.utils.timezone import now
from base.models import Product, Price
from decimal import Decimal
from requests.exceptions import RetryError, ConnectTimeout, ConnectionError
from simplejson.errors import JSONDecodeError
from fake_useragent import UserAgent


def header_updater():
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    return header


def updater(vendor_code, market_id, original_url, name, rubric_id, picture, price):
    try:
        product_to_save = Product.objects.get(vendor_code=vendor_code, market_id=market_id)
        product_to_save.original_url = original_url
        product_to_save.name = name
        product_to_save.rubric_id = rubric_id
        product_to_save.picture = picture
        product_to_save.last_update = now()
        if price == 0:
            product_to_save.temporary_preparse_available = False
        else:
            product_to_save.temporary_preparse_available = True
        product_to_save.save()
        price = Decimal(price)
        try:
            p = Price.objects.filter(product_id=product_to_save.pk).order_by('-created')[0]
            if p.value == price:
                pass
            else:
                price_obj = Price(product_id=product_to_save.pk, value=price)
                price_obj.save()
        except Price.DoesNotExist:
            price_obj = Price(product_id=product_to_save.pk, value=price)
            price_obj.save()
    except Product.DoesNotExist:
        product_to_save = Product(name=name, market_id=market_id, rubric_id=rubric_id, original_url=original_url,
                                  picture=picture, vendor_code=vendor_code, temporary_preparse_available=True,
                                  last_update=now())
        product_to_save.save()
        price = Decimal(price)
        price_obj = Price(product_id=product_to_save.pk, value=price)
        price_obj.save()


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        result = s[start:end]
        return result
    except ValueError:
        return "ValueError"


def make_retriable_request(url, retry, header):
    try:
        return requests.get(url, headers=header)
    except (ConnectTimeout, ConnectionError):
        print('connection error, retrying...' + url)
        if retry:
            retry -= 1
            return make_retriable_request(url, retry=retry, header=header)
        raise RetryError


def make_retriable_json_request(site_response, retry):
    try:
        return site_response.json()
    except JSONDecodeError:
        print('JSONDecodeError, retrying...')
        if retry:
            retry -= 1
            return make_retriable_json_request(site_response, retry=retry)
        raise RetryError


def resetter(market_id):
    obj_all = Product.objects.filter(market=market_id, available=True)
    for obj in obj_all:
        obj.temporary_preparse_available = False
        obj.save()


def preparse_to_available():
    obj_all = Product.objects.all()
    for obj in obj_all:
        if obj.temporary_preparse_available:
            obj.available = True
        else:
            obj.available = False
            try:
                p = Price.objects.filter(product_id=obj.pk).order_by('-created')[0]
                if p.value == 0:
                    pass
                else:
                    price_obj = Price(product_id=obj.pk, value=0)
                    price_obj.save()
            except Price.DoesNotExist:
                price_obj = Price(product_id=obj.pk, value=0)
                price_obj.save()
        obj.save()
