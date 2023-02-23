# Objetivo:
# Extraer las preguntas y sus descripciones de la página principal de stack overflow mediante web scraping usando beatifulSoup

# Pasos 
# 1) Definir URL semilla 
# 2) Realizar request a esa semilla 
# 3) Obtener respuesta del servidor 
# 4) Extraer datos del HTML 
# 5) Repetir paso 2 con nuevas URLs

import requests 
from bs4 import BeautifulSoup
url = "https://stackoverflow.com/questions"

# metemos los headers para que no nos baneen la ip 
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}


resp = requests.get(url,headers=headers)

soup = BeautifulSoup(resp.text,'html.parser')
container = soup.find(id='questions')


questionList = container.find_all(class_='s-post-summary--content')

print(questionList)

# sumaryList = container.find_all(class_='s-post-summary--content-excerpt')
# #print('sumaryList')
# #print(sumaryList)

questions = []
sumaries = []

for question in questionList :
    question_element = question.find('h3')
    sumary_element = question_element.find_next_sibling('div')

    question_text = question_element.text
    questions.append(question_text.strip())

    sumary_text = sumary_element.text
    sumaries.append(sumary_text.strip())

    print('\n')
    print(question_text.strip())
    print(sumary_text.strip())


    
# sumaries = []
# for sumary in sumaryList:
#     sumaries.append(sumary.text.replace('\n',' ').replace('\r',' ').strip())


# print('-------------')
# dictionary = dict(zip(questions, sumaries))
# print(dictionary)

