# OBJETIVO: 
#     - Extraer informacion sobre los productos en la pagina de Mercado Libre Mascotas
#     - Titulo, Precio, Descripcion
#     - Aprender a realizar extracciones verticales y horizontales utilizando reglas

# como compilar -> scrapy runspider mercadoLibre.py -o datos_de_salida.csv -t csv
# scrapy runspider mercadoLibre.py -o datos_de_salida -t csv

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class PageItem(Item):
    title = Field()
    price = Field()
    description = Field()


class ItemCrawler (CrawlSpider):
    name = 'Mi primer Spider'
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 20 
    }

    start_urls = ['https://listado.mercadolibre.com.ec/animales-mascotas/perros/']
    allowed_domains = ['articulo.mercadolibre.com.ec', 'listado.mercadolibre.com.ec']
    download_delay = 1

    rules = (
        # Para busqueda horizontal (paginacion)
        Rule(
            LinkExtractor(
                allow = r'/_Desde_'
            ),follow = True
        ),


        # Para búsqueda vertical de primer nivel 
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-'  #regex 
            ),

            follow = True, callback="parse_item" 
        ),
    )


    def parse_item (self,response):
        sel = Selector(response)
        item = ItemLoader(PageItem(), sel)


        item.add_xpath('title','//h1/text()')
        #item.add_xpath('price','//span[@class="andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact"]')
        item.add_xpath('price','//div[@class="ui-pdp-price__second-line"]//span[1]/text()') # se puede mejorar y obtner 3 consultas para el precio pero innecesario 
        item.add_xpath('description','//p[@class="ui-pdp-description__content"]/text()')

        yield item.load_item()
     
