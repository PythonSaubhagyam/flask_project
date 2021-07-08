# Import libraries
from sys import platform
from typing import Counter
from flask import Flask, request,jsonify,render_template
from mysql.connector.constants import ClientFlag
from datetime import datetime
import socket
import mysql.connector
import re 

app = Flask(__name__)

# Local Database connection
conn = mysql.connector.connect(
    host='localhost',
    port='8080',
    user='root',
    password='',
    database='cloudDb',
    charset='utf8')

# For Google Cloud SQL connection
'''
conn = {
    'user': 'root',
    'password': 'Password123',
    'host': '94.944.94.94',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}

# Now we establish our connection

cnxn = mysql.connector.connect(**config)
'''


@app.route('/')
def index():
    return "Welcome to programming world!!"

# Function for adding values into database
@app.route('/add')
def add_into_db():
    # Get IP address
    cursor = conn.cursor()
    hostname = socket.gethostbyname('facebook.com')
    # hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    var = str(IPAddr)
    first_visit = datetime.now()

    #Browser Version  and name 
    browser = request.user_agent.browser
    vers = request.user_agent.version
    
    last_visit = datetime.now()
    
    #Logic for Counter  
    SQL = "select ip_address from test_project"
    cursor.execute(SQL)
    var_fetch = cursor.fetchall()
    list_ =[]
    for i in var_fetch:
        a = re.sub(r"[\[]", "", str(i))
        b = re.sub(r"[,]", "", str(a))
        c = re.sub(r"[\()]", "", str(b))
        d = re.sub(r"[']", "", str(c))
        e = re.sub(r"[\"]", "", str(d))
        list_.append(e)
    l1=[]
    l2=[]
    l2.append(IPAddr)

    for i in l2:
        for j in list_:
            if i==j:
                l1.append(i)

    if len(l1)>0:
        update_db = "Update test_project Set counter = counter + 1 Where ip_address= %s"
        val2 = (IPAddr,)
        cursor.execute(update_db,val2)
    else:
        sql1 = "INSERT INTO test_project(ip_address,browser,browser_version,first_visit,last_visit) VALUES (%s,%s,%s,%s,%s)" # Insert values into database
        val1= (IPAddr,browser,vers,first_visit,last_visit)
        cursor.execute(sql1, val1)

    conn.commit()    
    show_data = {"Ip_address":IPAddr,"browser":browser,"browser_version":vers,"first_visit":first_visit,"last_visit":last_visit}
    # return jsonify({"Ip_address":IPAddr,"browser":browser,"browser_version":vers,"first_visit":first_visit,"last_visit":last_visit})   
    return render_template("index.html", show = show_data)
if __name__ == '__main__':
    app.run(debug=True, port=8000)