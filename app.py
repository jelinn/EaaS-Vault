import os
import hvac
import base64
from flask import Flask, g, request, render_template, redirect, jsonify
import boto3
import controller

app = Flask(__name__)

dynamo_client = boto3.client('dynamodb')
TableName='jlinn-demo-CustomerData'

@app.route('/')
def index():
  return render_template("index.html") 

@app.route('/view', methods=["GET","POST"])
def viewCustomers():
  rows = controller.dynamoReadItems()
  return render_template("viewCustomers.html", rows=rows)  

@app.route('/getCreds', methods=["GET"])
def getCredentials():
  client = controller.authDynamo()

@app.route('/decryptId',methods=["GET","POST"])    
def decryptCustomer():
  rows = controller.dynamoReadItems()
    # Call Vault to decrypt customerID, reassign to row, send to template to print
    #row = controller.decrypt 
  return render_template("decryptCustomers.html",rows=rows)

@app.route('/viewDecryptId',methods=["GET","POST"])
def decrypt():
  if request.form.get("decrypt"):
    print request.form.get("decrypt")
    decryptedId=controller.decryptVault(request.form.get("decrypt"))
    return decryptedId

@app.route('/add', methods=["GET","POST"])
def addCustomer():
  if request.method == 'POST':  
    providedName = request.form.get("name")
    customerNumber = request.form.get("idNumber")
    if request.form.get("encryptWithVault") == 'on':
      print("Encryption enabled - Calling Vault")
      #Make call to vault to encrypt
      encryptedCustomerNumber = controller.encryptVault(customerNumber)
      print("encrypted number = ", encryptedCustomerNumber)
      customerNumber = encryptedCustomerNumber['data']['ciphertext']
      print customerNumber 
    controller.dynamoCreateItem(providedName,customerNumber)   
    print("Record Added")  
  return render_template('addCustomers.html')



if __name__ == '__main__':
  app.run()
