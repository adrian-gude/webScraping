import requests
from lxml import html


# Pasos 
# 1) Definir URL semilla 
# 2) Realizar request a esa semilla 
# 3) Obtener respuesta del servidor 
# 4) Extraer datos del HTML 
# 5) Repetir paso 2 con nuevas URLs

url = "https://es.wallapop.com/coches-segunda-mano"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

resp = requests.get(url,headers=headers)

#print(resp.text)


# card-product-container
page = requests.get(url)
parser = html.fromstring(page.content)
print('--------')
print(parser)
# div[@class='card-product-product-info']
prices = parser.xpath("//div[@class='card-content']//span[@class='product-info-price']")
names = parser.xpath("//div[@class='card-content']//span[@class='product-info-title']")

auxPricesList = []
auxNamesList = []
for price in prices : 
    auxPricesList.append(price.text_content().strip())
    #print(price.text_content())

#print('Estoy final bucle')

for name in names :
    auxNamesList.append(name.text_content().strip())

# print("----------")
# print("Nombres : ")
# print(auxNamesList)
# print("Precios: ")
# print(auxPricesList)

print('-------------')
dictionary = dict(zip(auxNamesList, auxPricesList))
print(dictionary)

