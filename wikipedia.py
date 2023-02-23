import requests
from lxml import html


# Pasos 
# 1) Definir URL semilla 
# 2) Realizar request a esa semilla 
# 3) Obtener respuesta del servidor 
# 4) Extraer datos del HTML 
# 5) Repetir paso 2 con nuevas URLs

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

url = "https://www.wikipedia.org"

resp = requests.get(url,headers)
print(resp.text)

parser = html.fromstring(resp.text)


# english = parser.get_element_by_id("js-link-box-en")
# print(english.text_content())

# se puede obtener de otra manera con las expresiones xpath 
ingles = parser.xpath("//a[@id='js-link-box-en']/strong/text()")
print(ingles)

# intento de sacar todos los idiomas con un xpath 

# idiomas = parser.xpath("//div[contains(@class,'central-featured-lang')]//strong/text()")
# print(idiomas)

# for idioma in idiomas :
#     print(idioma)

idiomas = parser.find_class('central-featured-lang')

for idioma in idiomas: 
    print(idioma.text_content())