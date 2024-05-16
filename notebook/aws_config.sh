export AWS_ENDPOINT_URL=http://localhost.localstack.cloud:4566

aws sagemaker create-notebook-instance \
--notebook-instance-name notebook-s3-processing \
--instance-type ml.t3.large \
--role-arn arn:aws:iam::000000000000:role/s3-trigger-role \
--endpoint-url=$AWS_ENDPOINT_URL 

aws sagemaker create-presigned-notebook-instance-url --notebook-instance-name notebook-s3-processing --endpoint-url=$AWS_ENDPOINT_URL

# arn:aws:sagemaker:us-east-1:000000000000:notebook-instance/notebook-s3-processing
# notebook-s3-processing.notebook.us-east-1.sagemaker.aws