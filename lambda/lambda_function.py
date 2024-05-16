# aws lambda create-function \--function-name s3-trigger \
# --runtime python3.12 \
# --role arn:aws:iam::000000000000:role/s3-trigger-role \
# --handler lambda_function.lambda_handler \
# --zip-file fileb://function.zip \
# --endpoint-url=https://localhost.localstack.cloud:4566

import json

def lambda_handler(event, context):
    # Maneja el evento
    print("Evento recibido: " + json.dumps(event))
    # Realiza alguna acción, como procesar el archivo subido
    # Puedes acceder a los detalles del evento para obtener información sobre el archivo subido
