import logging
import os
from google.cloud import storage
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

def function_ejercicio_gcp(event, context):
    """Background Cloud Function to be triggered by Cloud Storage.
    """
    bucket_name = event["bucket"]
    file_name = event["name"]

    print(f"Event ID: {context.event_id}")
    print(f"Event type: {context.event_type}")
    print("Bucket: {}".format(bucket_name))
    print("File: {}".format(file_name))
    print("Metageneration: {}".format(event["metageneration"]))
    print("Created: {}".format(event["timeCreated"]))
    print("Updated: {}".format(event["updated"]))

    # Crear una instancia del cliente de Cloud Storage
    storage_client = storage.Client()

    # Obtener una referencia al cubo
    bucket = storage_client.get_bucket(bucket_name)

    # Obtener una referencia al Blob
    blob = bucket.blob(file_name)

    # Descargar el contenido del Blob
    content = blob.download_as_text()

    # Verificar si el archivo es un archivo CSV
    if file_name.endswith(".csv"):
        # Procesar el contenido CSV y cargar en BigQuery
        load_csv_to_bigquery(content)


def load_csv_to_bigquery(content):
    # Configurar las credenciales de BigQuery
    """
    # Descargar las credenciales desde Cloud Storage
    blob_cred = bucket_name.blob("dashboard-autofactura-3dee97686b51.json")
    creds_content = blob_cred.download_as_text()

    # Configurar las credenciales
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_content
    """
    # Configurar el cliente de BigQuery
    bigquery_client = bigquery.Client()

    # Configurar la referencia de dataset y tabla en BigQuery
    dataset_id = 'dashboard-autofactura.autofactura'
    table_id = 'dashboard-autofactura.autofactura.afben'
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    """    try:
        bigquery_client.get_table(table_ref)
    except NotFound:"""

    print(f"La tabla {table_id} no existe. Creando la tabla...")

    # Crear la tabla
    bigquery_client.create_table(

        table_ref,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True
    )

    # Configurar la carga de datos
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1

    # Cargar datos en BigQuery
    job = bigquery_client.load_table_from_file(
        content,
        table_ref,
        job_config=job_config,
    )

    # Esperar a que se complete la carga
    job.result()

    logging.info(f"Data loaded into BigQuery: {table_id}")