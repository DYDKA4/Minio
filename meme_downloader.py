import random
import string

import requests
from minio import Minio
from minio.error import S3Error
import uuid
from io import BytesIO
import time

# Конфигурация MinIO
minio_client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadminpassword",
    secure=False
)


bucket_name = "jokes"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

url = "https://v2.jokeapi.dev/joke/Any?type=single"


def get_random_joke():
    response = requests.get(url)
    if response.status_code == 200:
        joke_data = response.json()
        if joke_data['type'] == 'single':
            return joke_data['joke']
        elif joke_data['type'] == 'twopart':
            return f"{joke_data['setup']} ... {joke_data['delivery']}"
    else:
        return "Не удалось получить шутку."


def form_list_of_jokes():
    jokes = []
    for _ in range(10):
        joke = get_random_joke()
        jokes.append(joke)
    return jokes


def generate_1mb_random_text(size=1):
    size_in_bytes = 1048576 * size  # 1 МБ = 1048576 байт

    generated_text = ''.join(
        random.choices(string.ascii_letters + string.digits + string.punctuation + ' ', k=size_in_bytes))

    return generated_text

def create_and_upload_file():
    jokes = form_list_of_jokes()

    joke_text = "\n".join(jokes)
    file_name = f"jokes.txt"
    byte_data = joke_text.encode('utf-8')
    minio_client.put_object(
        bucket_name,
        file_name,
        BytesIO(byte_data),
        len(byte_data)
    )

def create_and_trash(size):
    file_name = f"{uuid.uuid4()}.txt"
    byte_data = generate_1mb_random_text(size).encode('utf-8')
    minio_client.put_object(
        bucket_name,
        file_name,
        BytesIO(byte_data),
        len(byte_data)
    )

if __name__ == "__main__":
    try:
        create_and_upload_file()
        while True:
            create_and_trash(1)
            print("Upload trash")
            time.sleep(2)
    except S3Error as e:
        if e.code == "XMinioAdminBucketQuotaExceeded":
            print(f"Ошибка: квота бакета '{bucket_name}' превышена. Завершаем работу.")
        else:
            print(f"Произошла ошибка MinIO: {e}")
    try:
        print("Uploading 5MB trash")
        create_and_trash(5)
    except S3Error as e:
        if e.code == "XMinioAdminBucketQuotaExceeded":
            print(f"Ошибка: квота бакета '{bucket_name}' превышена. Завершаем работу.")
        else:
            print(f"Произошла ошибка MinIO: {e}")

