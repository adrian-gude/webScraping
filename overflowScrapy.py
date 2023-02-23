# Objetivo:
# Extraer las preguntas y sus descripciones de la página principal de stack overflow mediante scrapy
# como compilar 
# scrapy runspider overflowScrapy.py -o prueba.csv -t csv

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class Question (Item) : 
    id = Field()
    question  = Field() 
    sumary = Field() 


class StackOverflow(Spider) : 
    name = 'Mi primer Spider'
    custom_settings = {
         'USER-AGENT ': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = ['https://stackoverflow.com/questions']

    
    def parse(self, response) : 
        sel = Selector(response)
        questions = sel.xpath('//div[@id="questions"]//div[@class="s-post-summary--content"]')
        
        for k,question in enumerate(questions) : 
            item = ItemLoader(Question(), question)
            item.add_xpath('question', './/h3/a/text()')
            item.add_xpath('sumary','.//div[@class="s-post-summary--content-excerpt"]/text()')
            item.add_value('id',k)

            yield item.load_item()