import requests
# traer la funcion html para convertir html a un archivo para aplicar xpath
import lxml.html as html
import os
import datetime

WEBSITE_URL  = 'https://www.elpalaciodehierro.com/electronica/computadoras/laptops/'
MAIN_URL= 'https://www.elpalaciodehierro.com'

XPATH_LINK_TO_ARTICLE = '//a[@class="b-product_tile-image"]/@href'
XPATH_PRODUCT_BRAND = '//h2[@class="b-product_main_info-brand"]/text()'
XPATH_PRODUCT_TITLE = '//div[@class="b-product_description-title"]/text()'
XPATH_PRODUCT_PRICE_OLD = '//div[@class="b-product_price-old"]/div/span[@class="b-product_price-value"]/text()'
XPATH_PRODUCT_PRICE_SALES = '//span[@class="b-product_price-value" and @content>1]/@content'
XPATH_AVAILABILITY = '//div[@class="b-product_main_info-availability"]/div/div/div/p/text()'

# arreglar diferencia entre nombres de clases de articulos que tienen descuento y los que no


def parse_article(link, today, f):
    try:
        # print(link)
        response = requests.get(link)

        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                brand = parsed.xpath(XPATH_PRODUCT_BRAND)[0]
                brand = brand.replace('\"', '')
                title = parsed.xpath(XPATH_PRODUCT_TITLE)[0]
                title = title.replace('\"', '')
                title = title.replace('/', '')
                title = title.replace(':', '')
                title = title.replace('"', '')
                sales_price = parsed.xpath(XPATH_PRODUCT_PRICE_SALES)[0]
                sales_price = sales_price.replace('\"', '')
                sales_price = sales_price.replace(',', '')
                sales_price = float(sales_price)
                availability = parsed.xpath(XPATH_AVAILABILITY)[0]
                availability = availability.replace('\"', '')
                # cpu = ''
                # gpu = ''
                # old_price = parsed.xpath(XPATH_PRODUCT_PRICE_OLD)[0]
                # old_price = old_price.replace('\"', '')
                # old_price = old_price.replace('$', '')

            except IndexError:
                print(f'Error article {link}')
                return

            if sales_price <= 150000.0:
                f.write(f'{brand}')
                f.write(title)
                # f.write(f'Old price: ${old_price}')
                f.write(f'Current price: ${sales_price}')
                f.write(availability)
                f.write(f'Url: {link}')
                f.write('\n\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(WEBSITE_URL)
        if response.status_code == 200:
            home = response.content.decode()
            parsed = html.fromstring(home)
            link_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%d-%m-%Y')

            local_path = f'./data/{today}'
            if not os.path.isdir(local_path):
                os.mkdir(local_path)
            else:
                print('folder already exist')
            
            print('Loading data...')
            with open(f'data/{today}/prueba.txt', 'w', encoding='utf-8') as f:
                for link in link_to_notices:
                    parse_article(MAIN_URL + link, today, f)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()