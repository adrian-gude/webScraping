from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

#driver = webdriver.Chrome('/Users/adrianlopezgude/chromedriver_mac64/chromedriver') # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER
options = Options()
options.add_argument(
    "user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'"
)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Voy a la pagina que requiero
driver.get('https://www.olx.com.ar/cars_c378')





for i in range(3): # Voy a darle click en cargar mas 3 veces
    try:
        boton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//button[@data-aut-id="btnLoadMore"]'))
        )
        print('boton', boton)

        boton.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH,'//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemTitle"]'))
        )

        #boton = driver.find_elements('xpath', '//button[@data-aut-id="btnLoadMore"]')
    except:
        print("estoy aqui")
        # si hay algun error, rompo el lazo. No me complico.
        break



cars = driver.find_elements('xpath', '//li[@data-aut-id="itemBox"]')

# Recorro cada uno de los anuncios que he encontrado
for car in cars:

    description = car.find_element('xpath', './/span[@data-aut-id="itemTitle"]').text
    print (description)
    price = car.find_element('xpath', './/span[@data-aut-id="itemPrice"]').text
    print (price)

#     details = car.find_element('xpath', './/span[@data-aut-id="itemDetails"]').text
#     print (details)

    # Por cada anuncio hallo la descripcion
    

   