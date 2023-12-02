leimport boto3
from itertools import product


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')


name = "thing"
email = "example"
email2 = "@thing.com"
passwords = [
    "012345",
    "123456",
    "234567",
    "345678",
    "456789",
    "567890",
    "678901",
    "789012",
    "890123",
    "901234"
]
for i in range(10):

    table.put_item(
                    Item={
            'user_name': name +str(i),   
            'email': email+str(i) + email2,
            'password': passwords[i]
                }
            )
