from flask import Flask, render_template, redirect, url_for,request,flash
from flask_mysqldb import MySQL

app=Flask(__name__)



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'
app.config['SECRET_KEY'] = 'the random string' 

mysql = MySQL(app)




@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM data")
    data = cur.fetchall()
    print(data)
    cur.close()

    return render_template("index.html", datas=data)





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE data
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('index'))





@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM data WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('index'))



@app.route('/insert', methods=['POST'])
def insert():
    if request.method=="POST":
        flash("Data Inserted Successfully")
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO data (name,email, phone) VALUES (%s,%s,%s)",
        (name, email,phone))
        mysql.connection.commit()
        return redirect(url_for('index'))




if __name__=="__main__":
    app.run(debug=True)