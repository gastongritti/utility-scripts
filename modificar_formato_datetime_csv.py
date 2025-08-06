import pandas as pd
from datetime import datetime
import chardet


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)
    result = chardet.detect(raw_data)
    encoding = result['encoding']

    if encoding is None:
        return 'utf-8'

    return encoding

file_path = 'event_log.csv'
encoding = detect_encoding(file_path)
print(f'Encoding detectado: {encoding}')

df = pd.read_csv(file_path, encoding=encoding)
reemplazos = 0
no_reemplazos = 0

for i, fila in df.iterrows():
    valor = fila["DATE_TIME"]

    try:
        fecha = datetime.strptime(valor, "%d/%m/%Y %H:%M:%S")
        valor = datetime.strftime(fecha, "%d/%m/%Y %I:%M:%S %p")
        valor = valor.replace('AM', 'a.m.').replace('PM', 'p.m.')
        df.at[i, 'DATE_TIME'] = valor
        reemplazos += 1
    except:
        no_reemplazos += 1

# Guardar el DataFrame modificado en un nuevo archivo CSV
df.to_csv('event_log_modificado.csv', index=False, encoding=encoding)

print(f'Cantidad de reemplazos realizados: {reemplazos}')
print(f'Cantidad de valores no reemplazados: {no_reemplazos}')


