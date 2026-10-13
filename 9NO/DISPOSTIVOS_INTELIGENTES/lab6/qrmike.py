import io
import qrcode
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

def generar_qr_en_memoria(data: str) -> io.BytesIO:
    """Genera un código QR y lo guarda en un buffer de memoria."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guardamos la imagen en un buffer de bytes en lugar de un archivo físico
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)  # Rebobinamos el buffer para que boto3 lea desde el inicio
    return buffer

def subir_a_minio(buffer: io.BytesIO, nombre_archivo: str):
    """Conecta con MinIO y sube el buffer de bytes."""
    # Configuración del cliente S3 apuntando a MinIO
    s3_client = boto3.client(
        's3',
        endpoint_url='http://localhost:9000',
        aws_access_key_id='admin',
        aws_secret_access_key='passwordseguro123',
        config=Config(signature_version='s3v4'),
        region_name='us-east-1' # MinIO requiere una región, aunque sea ficticia
    )

    bucket_name = 'qr-images-bucket'

    # Evaluación y creación del bucket si no existe
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"[EVALUACIÓN] El bucket '{bucket_name}' ya existe.")
    except ClientError:
        print(f"[EVALUACIÓN] El bucket no existe. Creando '{bucket_name}'...")
        s3_client.create_bucket(Bucket=bucket_name)

# Subida del archivo desde la memoria
    print(f"[EVALUACIÓN] Subiendo '{nombre_archivo}' a MinIO...")
    s3_client.upload_fileobj(
        buffer,
        bucket_name,
        nombre_archivo,
        ExtraArgs={'ContentType': 'image/png'}
    )
    print(f"[ÉXITO] El archivo fue subido correctamente.")
    print(f"[ACCESO] Puede verlo en la consola web: http://localhost:9001")

if __name__ == "__main__":
    # Datos que contendrá el QR
    datos_qr = "https://github.com/mikecardona076"
    nombre_imagen = "qr_sr_mike.png"

    print("--- INICIO DE PRÁCTICA MINIO + PYTHON ---")
    buffer_qr = generar_qr_en_memoria(datos_qr)
    subir_a_minio(buffer_qr, nombre_imagen)
    print("--- FIN DE LA PRÁCTICA ---")