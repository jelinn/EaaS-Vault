import boto3

dynamo_client = boto3.client('dynamodb')


def create_item(name,id):
  response = dynamo_client.put_item(
    TableName='jlinn-demo-CustomerData',
    Item={'customerName':{"S": name}, 'customerId':{"S":id} }
  )

def read_items():
  return dynamo_client.scan(
    TableName = 'jlinn-demo-CustomerData'
  )
