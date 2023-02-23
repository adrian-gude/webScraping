# Objetivo:
# Extraer 
# como compilar -> scrapy runspider tripScrapingVertical.py -o datos_de_salida.csv -t csv
# scrapy runspider tripScrapingVertical.py -o datos_de_salidaa -t csv

# https://www.tripadvisor.com/Hotels-g187508-Santiago_de_Compostela_Province_of_A_Coruna_Galicia-Hotels.html

# https://www.tripadvisor.com/Hotel_Review-g187508-d1567905-Reviews-Casa_Rural_Os_Vilares-Santiago_de_Compostela_Province_of_A_Coruna_Galicia.html
# https://www.tripadvisor.com/Hotel_Review-g187508-d195761-Reviews-Parador_de_Santiago_de_Compostela-Santiago_de_Compostela_Province_of_A_Coruna_Galicia.html

# https://www.tripadvisor.com/Attractions-g187508-Activities-Santiago_de_Compostela_Province_of_A_Coruna_Galicia.html




from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Hotel(Item):
    name = Field()
    score = Field() # El precio ahora carga dinamicamente. Por eso ahora obtenemos el score del hotel
    description = Field()
    amenities = Field()


class TripAdvisor(CrawlSpider): 
    name = 'Mi primer Spider'
    custom_settings = {
         'USER-AGENT ': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    
    start_urls = ['https://www.tripadvisor.com/Hotels-g187508-Santiago_de_Compostela_Province_of_A_Coruna_Galicia-Hotels.html']

    download_delay = 2 # tiempo que espera scrapy entre requerimientos para que no nos baneen la ip

    # reglas que definen a que links dentro de URL semilla tiene que ir mi spider en busca de info
    rules = (
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-'  #regex 
            ),

            follow = True, callback="parse_hotel" 
        ),
    )
    
    

    def parse_hotel(self, response): 
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        item.add_xpath('name', '//h1[@id="HEADING"]/text()')
        item.add_xpath('score', '//div[@class="grdwI P"]/span/text()')
        item.add_xpath('description', '//div[@class="fIrGe _T"]//text()',MapCompose(lambda i: i.replace('\r', '\n')))
        item.add_xpath('amenities','//div[@data-test-target="amenity_text"]/text()')


        yield item.load_item()



