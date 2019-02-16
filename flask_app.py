import request
import os
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
      #TODO - finish this 
      #Make call to vault to encrypt
    with sqlite3.connect('DATABASE') as con:
      cur = con.cursor()
      cur.execute("INSERT INTO customers (name, idNumber) VALUES (?,?)", (providedName, customerNumber))
      con.commit()
      print("Record Added")  
  return render_template('addCustomers.html')


if __name__ == '__main__':
  app.run()
