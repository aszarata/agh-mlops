import os
import boto3

S3 = boto3.resource("s3")
BUCKET = "sentiment-app-aszarata-lab"
S3_FOLDER = 'model'
LOCAL_FOLDER = 'model'


def download_s3_folder(bucket_name, s3_folder, local_dir):
    bucket = S3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=s3_folder):
        target = obj.key if local_dir is None else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == "/":
            continue
        bucket.download_file(obj.key, target)


if __name__ == "__main__":
    download_s3_folder(BUCKET, S3_FOLDER, LOCAL_FOLDER)