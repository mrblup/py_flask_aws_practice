import logging
import boto3
from botocore.exceptions import ClientError
import os
import requests
from boto3.dynamodb.conditions import Key
import json


def upload_image(bucket_name, key_name,url):
    r = requests.get(url, stream=True)

    session = boto3.Session()
    s3 = session.resource('s3')


    bucket = s3.Bucket(bucket_name)
    bucket.upload_fileobj(r.raw, key_name)

if __name__  == "__main__":
    x = open("static/a1.json")
    data = json.load(x)
    for i in data["songs"]:

        upload_image("s3895697-music-images", i["artist"]+".jpg",i["img_url"])