"""Genera HTML estático a partir de las rutas Flask para GitHub Pages."""
from pathlib import Path
from app import app

DESTINO = Path(__file__).resolve().parent / "avance10"
RUTAS = {"/": "index.html", "/productos": "productos.html",
         "/clientes": "clientes.html", "/proveedores": "proveedores.html",
         "/facturacion": "facturacion.html"}

def exportar():
    DESTINO.mkdir(exist_ok=True)
    with app.test_client() as client:
        for ruta, archivo in RUTAS.items():
            respuesta = client.get(ruta)
            if respuesta.status_code != 200:
                raise RuntimeError(f"Error al exportar {ruta}: {respuesta.status_code}")
            html = respuesta.get_data(as_text=True)
            for origen, destino in RUTAS.items():
                html = html.replace(f'href="{origen}"', f'href="{destino}"')
            html = html.replace('"/static/', '"../static/')
            if "{%" in html or "{{" in html:
                raise RuntimeError("Plantilla sin renderizar")
            (DESTINO / archivo).write_text(html, encoding="utf-8")
    print("GitHub Pages actualizado: cinco páginas en avance10/.")

if __name__ == "__main__":
    exportar()
