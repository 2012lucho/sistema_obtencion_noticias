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

ID_DIARIO = 1

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

    for elemento in elementos:
        html_data = BeautifulSoup(str(elemento.contents), 'html.parser')
        try:
            nota = {
                "enlace": html_data.find("a").get("href")
            }
        except:
            print("error, ignorando registro ")
            continue
        print(nota)
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