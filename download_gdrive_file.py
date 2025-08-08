from googleapiclient.discovery import build
from google.oauth2 import service_account

# Ruta al archivo service_account.json
SERVICE_ACCOUNT_FILE = "service_account.json"

# ID del archivo en Google Drive (lo que está entre /d/ y /view en el enlace)
FILE_ID = "TU_FILE_ID_AQUI"

# Nombre con el que se va a guardar localmente
DEST_FILE = "archivo_prueba.csv"

# Alcances necesarios para leer archivos de Drive
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def main():
    # Autenticación con la cuenta de servicio
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    # Construir el cliente de la API
    service = build("drive", "v3", credentials=creds)

    # Descargar el archivo
    request = service.files().get_media(fileId=FILE_ID)
    fh = open(DEST_FILE, "wb")
    downloader = build("drive", "v3", credentials=creds)._http.request
    from googleapiclient.http import MediaIoBaseDownload
    import io

    fh = io.FileIO(DEST_FILE, "wb")
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Descarga {int(status.progress() * 100)}%")

    print(f"Archivo descargado como: {DEST_FILE}")

if __name__ == "__main__":
    main()
