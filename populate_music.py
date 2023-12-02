import json
import boto3
x = open("static/a1.json")
data = json.load(x)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('music')
# x.close()
# for i in data['songs']:
#     print(i)


# for i in data["songs"]:

#     table.put_item(
#                     item = {
#                         "title": i["title"],
#                         "artist": i["artist"],
#                         "year": i["year"],
#                         "web_url": i["web_url"],
#                         "img_url": i["img_url"]

#                     }
#             )
#     print(i["title"])

with table.batch_writer() as batch:
    for i in data["songs"]:
        batch.put_item(Item = {
            
                        "title": i["title"],
                        "artist": i["artist"],
                        "year": i["year"],
                        "web_url": i["web_url"],
                        "img_url": i["img_url"]

                    
        })
