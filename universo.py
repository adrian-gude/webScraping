# Objetivo obtener titular y descripcion del diario universo de deportes con scrapy 

# Pasos 
# 1) Definir abtracción de Items 
# 2) Definir la clase Spider con los settings adecuados 
    # 3) Definir funcion parse
from bs4 import BeautifulSoup
from scrapy import Field, Item, Selector, Spider
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

#por defecto no se por que el csv me lo da en orden alfabético y no en el orden que aparece definido en la clase new


class New (Item):
    id = Field()
    title  = Field()
    description = Field()

class UniversoSpider (Spider):
    name = 'Spider para el diario Universo'
    custom_settings = {
         'USER-AGENT ': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = ['https://www.eluniverso.com/deportes/']


    def parse(self,response): 
        sel = Selector(response)
        news = sel.xpath('//div[@class="content-feed | space-y-2 "]/ul/li')

        for k,new in enumerate(news) : 
            item = ItemLoader(New(), new)
            item.add_value('id', k)
            item.add_xpath('title', './/h2/a/text()')
            item.add_xpath('description', './/p/text()')

            yield item.load_item()

    
    # con BeatifulSoup 
    # def parse(self, response) : 
    #     soup = BeautifulSoup(response.body)
    #     contenedor_noticias = soup.find_all('div',class_='//div[@class="content-feed | space-y-2 "]/ul/li')

    #     for contenedor in contenedor_noticias:
    #       noticias = contenedor.find_all(class_='relative', recursive = False)
    #       for noticia in noticias:
    #         item = ItemLoader(New(), response.body)
    #         titular = noticia.find('h2').text.replace('\n', '').replace('\r', '')
    #         descripcion = noticia.find('p')
    #         if (descripcion):
    #           item.add_value('descripcion', descripcion.text.replace('\n', '').replace('\r', ''))
    #         else:
    #           item.add_value('descripcion', 'N/A')
    #         item.add_value('titular', titular)
    #         item.add_value('id', id)
    #         id += 1
    #         yield item.load_item()
        
    

# para ejecutar scrapy runspider universo.py -o prueba.csv -t csv
# o definimos nuestro proceso 


process = CrawlerProcess({
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'datos_de_salida.csv'
})
process.crawl(UniversoSpider)
process.start()