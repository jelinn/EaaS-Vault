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
  return client.write('transit/encrypt/my-key',plaintext = base64.b64encode(plainText)

def decryptVault(cipherText):
  client = authVault()
  return writeVault('transit/decrypt/my-key',ciphertext=cipherText) 

def authVault():
  client = hvac.Client(url=os.environ['VAULT_ADDR'], token=os.environ['VAULT_TOKEN'])
  assert client.is_authenticated()
  return client

def dynamoCreateItem(name,id):
  response = dynamo_client.put_item(
    TableName='jlinn-demo-CustomerData',
    Item={'customerName':{"S": name}, 'customerId':{"S":id} }
  )

def dynamoReadItems():
  return dynamo_client.scan(
    TableName = 'jlinn-demo-CustomerData'
  )
