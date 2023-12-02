import boto3

def make_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')


    table = dynamodb.create_table(
    TableName='music',
    KeySchema=[
        {
            'AttributeName': 'title',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'artist',
            'KeyType': 'RANGE'
        }   
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },
              {
            'AttributeName': 'artist',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
    )
    return table



if __name__ == "__main__":
    something = make_table()
    print("Table status:", something.table_status)




