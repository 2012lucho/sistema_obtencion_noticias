#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import datetime
import sys

#sys.path.insert(1, "./modulos")
sys.path.insert(1, "../../modulos")
from clientecoordinador import *
cliente = ClienteCoordinador()

ID_DIARIO = 6
BASE_URL  = "https://www.diariouno.com.ar"

fecha = datetime.datetime.now().strftime("%Y%m%d")

diccio_nam = {}

headers_ = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
}

def procesar_elementos( url, cat_id, categoria ):
    print(url, cat_id, categoria)
    cantidad = 0
    pagina   = 1
    
    response = requests.get(url, headers=headers_, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    elementos = soup.find_all("article")

    listado_noticias = []

    for elemento in elementos:
        html_data = BeautifulSoup(str(elemento.contents), 'html.parser')
        try:
            nota = {
                "enlace": html_data.find("a").get("href"),
                "category": cat_id,
                "id_diario": ID_DIARIO,
            }

            print("Haciendo peticion a nota especifica ", nota["enlace"])

            response_esp = requests.get(nota["enlace"], headers=headers_, timeout=10)
            soup_esp = BeautifulSoup(response_esp.text, 'html.parser')

            nota["titulo"] = soup_esp.find(class_="article-title").find("h1").text
            cont_part = soup_esp.find_all(class_="article-body")

            nota["contenido"] = ""
            for cont in cont_part:
                nota["contenido"] = cont.decode_contents()
            
            listado_noticias.append(nota)

            with open('./resultados/'+fecha+'_'+str(ID_DIARIO)+'.json', 'w') as file:
                json.dump(listado_noticias, file)
                print('guardado archivo '+fecha+'_'+str(ID_DIARIO)+'.json')
        except Exception as e:
            print("error, ignorando registro ", e)
            continue
        print(nota)
        print("")
        cantidad = cantidad + 1

    return cantidad

total = 0
for categoria in CATEGORIAS:
    if (categoria == CATEGORIA_INICIO or CATEGORIAS[categoria]["category"] == CATEGORIA_INICIO_ID):
        print(categoria, CATEGORIA_INICIO, CATEGORIA_INICIO_ID)
        PROCESAR = True
        continue    
    
    if (PROCESAR == True):
        print("Procesado categoria: ",categoria)
        url = CATEGORIAS[categoria]['url']
        total = total + procesar_elementos( url, CATEGORIAS[categoria]["category"],  categoria )
    else:
        print("ignorando categoria: ", categoria)
        continue

print(total)