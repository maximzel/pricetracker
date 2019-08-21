import os
from base.utilities import header_updater, updater, find_between, make_retriable_request, make_retriable_json_request, resetter


sites_utko = [['15', 'https://www.utkonos.ru/utkax.php/cat/more/4472'],
            ['2', 'https://www.utkonos.ru/utkax.php/cat/more/27'],
            ['1', 'https://www.utkonos.ru/utkax.php/cat/more/10'],
            ['3', 'https://www.utkonos.ru/utkax.php/cat/more/7'],
            ['7', 'https://www.utkonos.ru/utkax.php/cat/more/77'],
            ['2', 'https://www.utkonos.ru/utkax.php/cat/more/40'],
            ['9', 'https://www.utkonos.ru/utkax.php/cat/more/65'],
            ['8', 'https://www.utkonos.ru/utkax.php/cat/more/4405'],
            ['6', 'https://www.utkonos.ru/utkax.php/cat/more/52'],
            ['4', 'https://www.utkonos.ru/utkax.php/cat/more/98'],
            ['12', 'https://www.utkonos.ru/utkax.php/cat/more/248'],
            ['12', 'https://www.utkonos.ru/utkax.php/cat/more/1722'],
            ['13', 'https://www.utkonos.ru/utkax.php/cat/more/907'],
            ['11', 'https://www.utkonos.ru/utkax.php/cat/more/421'],
            ['14', 'https://www.utkonos.ru/utkax.php/cat/more/320'],
            ['13', 'https://www.utkonos.ru/utkax.php/cat/more/5542'],
            ['12', 'https://www.utkonos.ru/utkax.php/cat/more/606']]
retries = 2


def parse_utko():
    header = header_updater()
    print(header)
    resetter(market_id=2)
    for value_1, value_2 in sites_utko:
        url_for_items_amount_check = value_2 + '/page/1'
        url_for_items_amount_check_response = make_retriable_request(url_for_items_amount_check, retry=retries, header=header)
        items_amount_check = make_retriable_json_request(url_for_items_amount_check_response, retry=retries)
        items_amount = items_amount_check['content']
        pages = find_between(items_amount, '<div class="signature">Страница: 1 из ', '</div></div>')
        pages = int(pages)
        for page in range(1, pages + 1):
            site_address = f'{value_2}/page/{str(page)}'
            print(site_address)
            site_address_response = make_retriable_request(site_address, retry=retries, header=header)
            response_decoded = make_retriable_json_request(site_address_response, retry=retries)
            products_list_raw_code_html = response_decoded['content']
            products_list_raw_code = products_list_raw_code_html.split('<div class="goods_view_box-view goods_view goods_view-item"')
            for prod in products_list_raw_code[1:]:
                prod_values = find_between(prod, 'name="log_json" value=', '>')
                prod_values = prod_values.replace('&quot;', '"')
                title = find_between(prod_values, '"name":"', '","')
                title = title.replace('\\', '')
                url_path = find_between(prod, '<a href="', '"')
                url = 'https://www.utkonos.ru' + url_path
                img_path = find_between(prod, '<img src="', '"').split('?')[0]
                img_url = 'https://www.utkonos.ru' + img_path
                vendor_code = find_between(prod_values, '"id":"', '"')
                img_file_format = img_path.split('.')[-1]
                img = vendor_code + '.' + img_file_format
                price = find_between(prod_values, '"price":"', '"')
                if os.path.isfile(os.path.abspath(os.path.join("")) + '/static/media/product/utkonos/' + img):
                    pass
                else:
                    img_object = make_retriable_request(img_url, retry=retries, header=header)
                    with open(os.path.abspath(os.path.join("")) + '/static/media/product/utkonos/' + img, 'wb') as file:
                        file.write(img_object.content)
                        file.close()
                        print('file created: ' + img)
                img_local_path = '/product/utkonos/' + img
                updater(vendor_code=vendor_code, market_id=2, original_url=url, name=title, rubric_id=value_1,
                        picture=img_local_path, price=price)
