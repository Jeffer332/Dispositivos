# Instalación de dependencias adicionales
!pip install beautifulsoup4 requests pandas tabulate matplotlib

# Importar librerías necesarias
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from tabulate import tabulate

# Función para procesar los datos de la tabla en HTML
def processTableData(tbl):
    rows = []
    for row in tbl.find('tbody').find_all('tr'):  # Itera sobre cada fila de la tabla
        cells = [cell.text.strip() for cell in row.find_all(['td', 'th'])]  # Extrae el texto de cada celda
        if cells:
            rows.append(cells)
    return rows

# Leer el sitio web
url = 'https://es.wikipedia.org/wiki/Anexo:Tabla_estad%C3%ADstica_de_la_Copa_Mundial_de_F%C3%BAtbol'
response = requests.get(url)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    soup = bs(response.content, 'html.parser')  # Procesa el HTML con BeautifulSoup
    table = soup.find_all('table')[0]  # Encuentra la primera tabla en el HTML

    # Extraer los datos de la tabla y convertirlos en un DataFrame
    table_data = processTableData(table)
    df = pd.DataFrame(table_data[1:], columns=table_data[0])  # Usa la primera fila como encabezado

    # Limpieza de datos y conversión de tipos
    df['Títulos'] = pd.to_numeric(df['Títulos'], errors='coerce')  # Convierte la columna 'Títulos' a numérico
    df['Rend.'] = df['Rend.'].str.replace('%', '').str.replace(',', '.').astype(float)  # Convierte la columna 'Rend.' a float

    # Presentación de la tabla en consola
    print("Tabla estadística de la Copa Mundial de Fútbol:")
    print(tabulate(df.head(20), headers='keys', tablefmt='fancy_grid', showindex=False))  # Muestra las primeras 10 filas de la tabla

    # Guardar en un archivo CSV
    df.to_csv('statsWorldCup.csv', index=False)
    print("\nArchivo CSV guardado con éxito.")

else:
    print(f"Error: No se pudo acceder al sitio web. Código de estado {response.status_code}")