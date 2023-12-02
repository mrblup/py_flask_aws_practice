
import key_config as keys
import boto3 
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client("s3")
def get_artist(song_name):
    table = dynamodb.Table('music')
    response = table.query(
                KeyConditionExpression=Key('title').eq(song_name)
        )
    
    items = response['Items']
    return items[0]["artist"]

# print(get_artist("Cat's in the Cradle"))

# response = s3.client.get_object(
#     Bucket='s3895697-music-images',
#     Key='fun..jpg',
# )

def gen_signed_url(bucket_name, object_name):
    url = s3.generate_presigned_url(ClientMethod='get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=3600)
    # print(url)
    return(url)


fe = Key('year').eq("2013")
pe = "#yr, title, artist"
# Expression Attribute Names for Projection Expression only.
ean = { "#yr": "year", }
esk = None

table = dynamodb.Table('music')
response = table.scan(
    FilterExpression=fe,
    ProjectionExpression=pe,
    ExpressionAttributeNames=ean
    )
print(response["Items"])
# print(gen_signed_url("s3895697-music-images","fun..jpg"))
# print(query_movies("2013"))
