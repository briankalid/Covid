# export AWS_ENDPOINT_URL=http://localhost.localstack.cloud:4566

aws iam create-role --role-name lambda-s3-trigger-role --assume-role-policy-document file://policy.json --endpoint-url=$AWS_ENDPOINT_URL

aws lambda create-function \
--function-name lambda-s3-trigger \
--runtime python3.12 \
--role arn:aws:iam::000000000000:role/s3-trigger-role \
--handler lambda_function.lambda_handler \
--zip-file fileb://function.zip \
--endpoint-url=$AWS_ENDPOINT_URL

aws s3api put-bucket-notification-configuration \
--bucket mexico-bucket \
--notification-configuration '{"LambdaFunctionConfigurations":[{"LambdaFunctionArn":"arn:aws:lambda:us-east-1:000000000000:function:lambda-s3-trigger","Events":["s3:ObjectCreated:*"]}]}' \
--endpoint-url=$AWS_ENDPOINT_URL