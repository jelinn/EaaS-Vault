import os
import hvac
import base64
from flask import Flask, g, request, render_template, redirect, jsonify
import boto3
import dynamo_controller

app = Flask(__name__)

dynamo_client = boto3.client('dynamodb')
TableName='jlinn-demo-CustomerData'

@app.route('/')
def index():
  return render_template("index.html") 

@app.route('/view', methods=["GET","POST"])
def viewCustomers():
  rows = dynamo_controller.read_items()
  return render_template("viewCustomers.html", rows=rows)  

@app.route('/add', methods=["GET","POST"])
def addCustomer():
  if request.method == 'POST':  
    providedName = request.form.get("name")
    customerNumber = request.form.get("idNumber")
    if request.form.get("encryptWithVault") == 'on':
      print("Encryption enabled - Calling Vault")
      #Make call to vault to encrypt
      client = hvac.Client(url=os.environ['VAULT_ADDR'], token=os.environ['VAULT_TOKEN'])
      assert client.is_authenticated()
      encryptedCustomerNumber = client.write('transit/encrypt/my-key', plaintext=base64.b64encode(customerNumber))
      print("encrypted number = ", encryptedCustomerNumber)
      customerNumber = encryptedCustomerNumber['data']['ciphertext']
      print customerNumber 
    dynamo_controller.create_item(providedName,customerNumber)   
    print("Record Added")  
  return render_template('addCustomers.html')


if __name__ == '__main__':
  app.run()
