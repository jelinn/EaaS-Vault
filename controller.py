import base64
import os
import boto3
import hvac

dynamo_client = boto3.client('dynamodb')

def readVault(path):
  client = authVault()
 
def writeVault(path,text):
  client = authVault()
  return client.write(path,plaintext=text)
   
def encryptVault(plainText):
  client = authVault()
  print base64.b64encode(plainText)
  return client.write('transit/encrypt/my-key',plaintext = base64.b64encode(plainText))

def decryptVault(cipherText):
  client = authVault()
  encodedText = client.write('transit/decrypt/my-key',ciphertext=cipherText) 
  return base64.b64decode(encodedText["data"]["plaintext"])

def getAwsCredential():
  client = authVault()
  return client.read('aws/creds/dynamo-role')

def authVault():
  client = hvac.Client(url=os.environ['VAULT_ADDR'], token=os.environ['VAULT_TOKEN'])
  assert client.is_authenticated()
  return client

def authDynamo():
  #vault_sesison = authVault()
  credential = getAwsCredential()
  print credential
  AWS_ACCESS_KEY=credential['data']['access_key']
  AWS_SECRET_KEY=credential['data']['secret_key']
  print("Access Key : ", AWS_ACCESS_KEY)
  print("SECRET KEY : ", AWS_SECRET_KEY)
  print("AWS Cred = ", credential)
  #dynamo_client = boto3.client('dynamodb',
  #                            aws_access_key_id=AWS_ACCESS_KEY,
  #                            aws_secret_access_key=AWS_SECRET_KEY,
  #                            region_name='us-east-2'
  #                            )  
  #return dynamo_client

def dynamoCreateItem(name,id):
  #dynamo_client = authDynamo()
  response = dynamo_client.put_item(
    TableName='jlinn-demo-CustomerData',
    Item={'customerName':{"S": name}, 'customerId':{"S":id} }
  )

def dynamoReadItems():
  return dynamo_client.scan(
    TableName = 'jlinn-demo-CustomerData'
  )
