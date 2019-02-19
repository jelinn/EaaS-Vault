import request
import os
import hvac
import base64
from flask import Flask, g, request, render_template, redirect, jsonify
from sqlite3 import dbapi2 as sqlite3

DATABASE = 'data.db'

app = Flask(__name__)

conn = sqlite3.connect('DATABASE')
print("Opened DB.")
conn.execute('CREATE TABLE IF NOT EXISTS customers(name TEXT, idNumber INT)')
print("Created Table")
conn.close()



@app.route('/view', methods=["GET","POST"])
def viewCustomers():
  conn = sqlite3.connect('DATABASE')
  conn.row_factory = sqlite3.Row
  print("opened DB for READ")
  cur=conn.cursor()
  cur.execute("SELECT * FROM customers")
  rows = cur.fetchall()
  return render_template("viewCustomers.html", rows=rows)  

@app.route('/add', methods=["GET","POST"])
def addCustomer():
  print request.method
  if request.method == 'POST':  
    providedName = request.form.get("name")
    customerNumber = request.form.get("idNumber")
    print(request.form.get("encryptWithVault"))
    if request.form.get("encryptWithVault") == 'on':
      print("Encryption enabled - Calling Vault")
      #Make call to vault to encrypt
      client = hvac.Client(url=os.environ['VAULT_ADDR'], token=os.environ['VAULT_TOKEN'])
      assert client.is_authenticated()
      encryptedCustomerNumber = client.write('transit/encrypt/my-key', plaintext=base64.b64encode(customerNumber))
      print("encrypted number = ", encryptedCustomerNumber)
      customerNumber = encryptedCustomerNumber['data']['ciphertext']
      print customerNumber 
    with sqlite3.connect('DATABASE') as con:
      cur = con.cursor()
      cur.execute("INSERT INTO customers (name, idNumber) VALUES (?,?)", (providedName, customerNumber))
      con.commit()
      print("Record Added")  
  return render_template('addCustomers.html')


if __name__ == '__main__':
  app.run()
