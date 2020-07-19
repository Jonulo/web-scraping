import requests
# traer la funcion html para convertir html a un archivo para aplicar xpath
import lxml.html as html
# Crear carpeta con fecha de hoy
import os
# Traer la fecha actual
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//div[@class="V_Trends"]/h2/a/@href'
XPATH_TITLE = '//h2/a[contains(@class, "") and not(@href)]/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link, today):
    try:
        print(link)
        response = requests.get(link)
        if response.status_code == 200:
            # Todo igual como en la función principal
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)
                # Hay titulos que vienen entre comillas, con lo siguiente como sabes que TITLE es un string
                # reemplazamos las comillas por NADA:
                title = title.replace('\"', '')
                title = title.replace('/', '')
                title = title.replace(':', '')
                title = title.replace('"', '')
                print(title)
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            # Este error se maneja porque hay noticia que no tienen SUMMARY y si pasa eso que no traiga
            # esa noticia y pase a la siguiente:
            except IndexError:
                print('error creating notice files')
                return

            # WITH es un manejador contextual que si el archivo se cierra por el script que no funciona
            # este manejador mantiene el archivo seguro para que no se corrompa.

            # today es la carpeta que se creo en la main function y dentro va la nueva noticia que se guardara
            # el segundo parametro es abrir el doc en modo escritura y el encoding para los caracteres especiales
            with open(f'data/{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        # si el requests es diferente de code 200
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            # Obtenemos el html y decode transforma caracteres especiales(ñ) en algo que python no tenga errores
            home = response.content.decode()
            # Toma el contenido html de home y lo transforma de forma que podemos usar XPATH
            parsed = html.fromstring(home)
            # Obtenemos una lista de resultados al aplicar XPATH ($x('...'))
            link_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(link_to_notices)

            # date trae una fecha y today() la de hoy. Y convertimos a cadenas de caracteres con el formato
            today = datetime.date.today().strftime('%d-%m-%Y')
            # Si no existe una carpeta con el nombre(fecha de hoy) entonces creala

            local_path = f'./data/{today}'
            if not os.path.isdir(local_path):
                os.mkdir(local_path)
            else:
                print('folder already exist')

            # por cada link la funcion entra y extrae la info de la noticia y lo guardara con fecha de hoy
            for link in link_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()