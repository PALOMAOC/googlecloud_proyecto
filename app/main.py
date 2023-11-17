import json
from google.cloud import storage
from google.cloud import firestore


def cloud_function_handler(data, context):
    # Obtiene el nombre del bucket y la clave del archivo JSON del evento de GCS
    bucket = data['bucket']
    key = data['name']
    print(bucket)
    print(key)

    # Descarga el archivo JSON desde GCS
    bucket_obj = storage_client.get_bucket(bucket)
    blob = bucket_obj.blob(key)
    json_data = blob.download_as_text()

    # Parsea el JSON
    data = json.loads(json_data)

    # Inserta los datos en Firestore
    db.collection('mi-ejercicio-gcp').document().set({
        'ID': data['ID'],
        'Nombre': data['Nombre'],
        'Correo electrónico': data['Correo electrónico'],
        'Fecha de registro': data['Fecha de registro']
    })
