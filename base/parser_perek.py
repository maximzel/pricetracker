import os
from math import ceil
from urllib.parse import urlsplit
from base.utilities import header_updater, updater, find_between, make_retriable_request, make_retriable_json_request, resetter


sites_perek = [['1', 'https://www.perekrestok.ru/catalog/moloko-syr-yaytsa'],
               ['2', 'https://www.perekrestok.ru/catalog/ovoschi-frukty-griby'],
               ['3', 'https://www.perekrestok.ru/catalog/myaso-ptitsa-delikatesy'],
               ['4', 'https://www.perekrestok.ru/catalog/zamorojennye-produkty'],
               ['5', 'https://www.perekrestok.ru/catalog/makarony-krupy-spetsii'],
               ['6', 'https://www.perekrestok.ru/catalog/hleb-sladosti-sneki'],
               ['7', 'https://www.perekrestok.ru/catalog/ryba-i-moreprodukty'],
               ['8', 'https://www.perekrestok.ru/catalog/kofe-chay-sahar'],
               ['9', 'https://www.perekrestok.ru/catalog/soki-vody-napitki'],
               ['2', 'https://www.perekrestok.ru/catalog/konservy-orehi-sousy'],
               ['11', 'https://www.perekrestok.ru/catalog/tovary-dlya-jivotnyh'],
               ['12', 'https://www.perekrestok.ru/catalog/krasota-gigiena-bytovaya-himiya'],
               ['13', 'https://www.perekrestok.ru/catalog/tovary-dlya-mam-i-detey'],
               ['14', 'https://www.perekrestok.ru/catalog/avto-dom-sad-kuhnya']]
retries = 2


def parse_perek():
    header = header_updater()
    print(header)
    resetter(market_id=1)
    for value_1, value_2 in sites_perek:
        url_for_items_amount_check = value_2 + '?page=1&sort=price_asc&ajax=true'
        url_for_items_amount_check_response = make_retriable_request(url_for_items_amount_check, retry=retries, header=header)
        items_amount_check = make_retriable_json_request(url_for_items_amount_check_response, retry=retries)
        items_amount = items_amount_check['count']
        pages = ceil(int(items_amount)/24)
        for page in range(1, pages):
            site_address = f'{value_2}?page={str(page)}&sort=price_asc&ajax=true'
            print(site_address)
            site_address_response = make_retriable_request(site_address, retry=retries, header=header)
            response_decoded = make_retriable_json_request(site_address_response, retry=retries)
            products_list_raw_code_html = response_decoded['html']
            products_list_raw_code = products_list_raw_code_html.split('<li class="js-catalog-product _additionals xf-catalog__item"')
            for prod in products_list_raw_code[1:]:
                title = find_between(prod, 'title="', '"')
                url_path = find_between(prod, '<a href="', '"')
                url = 'https://www.perekrestok.ru' + url_path
                img_path = find_between(prod, 'data-src="', '"')
                if 'http' in img_path:
                    img_url = img_path
                else:
                    img_url = 'https://www.perekrestok.ru' + img_path
                parts = urlsplit(url_path)
                vendor_code = parts.path.split('--')[-1]
                img_file_format = img_path.split('.')[-1]
                img = vendor_code + '.' + img_file_format
                if 'data-cost' in prod:
                    price_part = prod.split('data-cost')[-1]
                    price = find_between(price_part, '="', '"')
                else:
                    price = 0
                if os.path.isfile(os.path.abspath(os.path.join("")) + '/static/media/product/perekrestok/' + img):
                    pass
                else:
                    img_object = make_retriable_request(img_url, retry=retries, header=header)
                    with open(os.path.abspath(os.path.join("")) + '/static/media/product/perekrestok/' + img, 'wb') as file:
                        file.write(img_object.content)
                        file.close()
                        print('file created: ' + img)
                img_local_path = '/product/perekrestok/' + img
                updater(vendor_code=vendor_code, market_id=1, original_url=url, name=title, rubric_id=value_1,
                        picture=img_local_path, price=price)
