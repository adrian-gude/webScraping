"""
OBJETIVO: 
    - Extraer autor, texto e info
    - Extraer todas las opiniones de los usuarios que dejan reviews en hoteles de Santiago en tripadvisor
    - De la opinion me interesa el usuario,el titulo, la calificación y el contenido
    - Aprender a realizar extracciones de dos niveles de verticalidad y dos niveles de horizontalidad
    - Aprender a reducir el espectro de busqueda para filtrar URLs en las reglas
    - Evitar obtener URLs repetidas

"""


from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Opinion (Item):
    user = Field()
    title = Field()
    qualification = Field()
    content = Field()
    hotel = Field()


class TripAdvisor(CrawlSpider):
    name = 'TripAdvisorCrawler'
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 20 ,
      'FEED_EXPORT_FIELDS': ['user',
                            'title',
                            'qualification',
                            'content',
                            'hotel']
    }

    allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Hotels-g187508-Santiago_de_Compostela_Province_of_A_Coruna_Galicia-Hotels.html']

    download_delay = 1

    rules = (
        # Regla para horizontal de cada página de TripAdvisor 
        Rule(
            LinkExtractor(
                  allow=r'-oa\d+-' 
            ),follow = True
        ),

        # Regla para vertical de cada enlace del hotel
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                restrict_xpaths=['//a[@class="property_title prominent "]'],
            ),follow=True
        ),

        # Busqueda en las opiniones de forma horizontal
        # Opiniones del hotel 
        Rule(
            LinkExtractor(
                allow = r'-Reviews-or\d+-'
            ), follow = True
        ),

    Rule(
      LinkExtractor(
        allow=r'/Profile/',
        restrict_xpaths=['//div[@data-test-target="reviews-tab"]'],
      ), follow=True, callback='parse_opinion'),
  )

    def parse_opinion(self,repsonse):
        sel = Selector(repsonse)
        opinions_container = sel.xpath('//div[@id="content"]')
        user = sel.xpath('//h1/span/text()').get()

        for opinion in opinions_container : 
            item = ItemLoader(Opinion(), opinion)
            item.add_xpath('user', '//h1/span/text()')
            item.add_xpath('title', '//div[@class="AzIrY b _a VrCoN"]/text()')
            item.add_xpath('hotel', './/div[@title]/text()') 
            item.add_xpath('content', './/q/text()', MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
            item.add_xpath('qualification', './/div[contains(@class, "ui_card section")]//a/div/span[contains(@class, "ui_bubble_rating")]/@class', MapCompose(lambda i: i.split('_')[-1]))
            yield item.load_item()
      