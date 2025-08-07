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

for i, fila in df.iterrows():
    gcode = fila["G-CODE"]
    user = fila["USER"]

    if gcode == 'LADRILLO 12 IDA (ala 2.5).tap':
        gcode = gcode.replace('LADRILLO 12 IDA (ala 2.5).tap', 'PIEZA N50.tap')
        df.at[i, 'G-CODE'] = gcode

    if user == 'vboxuser':
        user = user.replace('vboxuser', 'Juan Perez')
        df.at[i, 'USER'] = user

# Guardar el DataFrame modificado en un nuevo archivo CSV
df.to_csv('event_log_example.csv', index=False, encoding=encoding)


