import json
from google.cloud import storage, firestore

# Create instances of the GCS client and Firestore client
gcs_client = storage.Client()
firestore_client = firestore.Client()

# Name of the Firestore collection
collection_name = 'mi-ejercicio-gcp'

def gcs_to_firestore(data, context):
    # Print the event data
    print(data)

    # Get the bucket name and object key from the event
    bucket = data['bucket']
    key = data['name']
    print(bucket)
    print(key)

    # Download the JSON file from GCS
    bucket_obj = gcs_client.bucket(bucket)
    blob = bucket_obj.blob(key)
    json_data = blob.download_as_text()

    # Parse the JSON
    data = json.loads(json_data)

    # Insert data into Firestore
    doc_ref = firestore_client.collection(collection_name).document()
    doc_ref.set({
        'ID': data['ID'],
        'Nombre': data['Nombre'],
        'Correo electrónico': data['Correo electrónico'],
        'Fecha de registro': data['Fecha de registro']
    })

    return 'Success'
 