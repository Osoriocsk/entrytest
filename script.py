#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup

def buscar_productos(palabra, limite=5):
    url = f"https://listado.mercadolibre.com.co/{palabra.replace(' ', '-')}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    items = soup.select("li.ui-search-layout__item")[:limite]

    resultados = []
    for item in items:
        titulo_tag = item.select_one("h2.ui-search-item__title")
        precio_entero = item.select_one("span.price-tag-fraction")
        precio_decimal = item.select_one("span.price-tag-cents")

        titulo = titulo_tag.get_text(strip=True) if titulo_tag else "SIN TÍTULO"
        if precio_entero:
            precio = precio_entero.get_text(strip=True)
            if precio_decimal:
                precio += f".{precio_decimal.get_text(strip=True)}"
            precio = f"${precio}"
        else:
            precio = "SIN PRECIO"

        resultados.append((titulo, precio))

    return resultados

if __name__ == "__main__":
   
    term = "laptop"
    try:
        prods = buscar_productos(term, limite=5)
    except Exception as e:
        print("Error al buscar:", e, file=sys.stderr)
        sys.exit(1)

    if not prods:
        print(f"No se encontraron resultados para '{term}'.")
    else:
        print(f"Top {len(prods)} resultados para '{term}':\n")
        for i, (t, p) in enumerate(prods, 1):
            print(f"{i}. {t}\n   Precio: {p}\n")
