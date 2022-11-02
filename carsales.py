from flask import Flask, render_template, request, redirect, url_for
import pyodbc, os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

carsales = Flask(__name__)
carsales.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def connection():
    s = 'TANHOANG\TANHOANG1' #Your server name 
    d = 'testdb' 
    u = 'sa' #Your login
    p = '123456' #Your login password
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn

@carsales.route("/")
def main():
    # cars = []
    labels = []
    conn = connection()
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM dbo.TblCars")
    cursor.execute("SELECT * FROM dbo.label")
    for row in cursor.fetchall():
        # cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
        labels.append({"id": row[0], "name": row[1]})
    conn.close()
    return render_template("labelslist.html", labels = labels)


@carsales.route("/addlabel", methods = ['GET','POST'])
def addcar():
    if request.method == 'GET':
        return render_template("addlabel.html", label = {})
    if request.method == 'POST':
        id = int(request.form["id"])
        name = request.form["name"]
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.label (id, name) VALUES (?, ?)", id, name)
        conn.commit()
        conn.close()
        return redirect('/')
        
@carsales.route('/updatecar/<int:id>',methods = ['GET','POST'])
def updatecar(id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM dbo.TblCars WHERE id = ?", id)
        for row in cursor.fetchall():
            cr.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
        conn.close()
        return render_template("addcar.html", car = cr[0])
    if request.method == 'POST':
        name = str(request.form["name"])
        year = int(request.form["year"])
        price = float(request.form["price"])
        cursor.execute("UPDATE dbo.TblCars SET name = ?, year = ?, price = ? WHERE id = ?", name, year, price, id)
        conn.commit()
        conn.close()
        return redirect('/')

@carsales.route('/deletecar/<int:id>')
def deletecar(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.TblCars WHERE id = ?", id)
    conn.commit()
    conn.close()
    return redirect('/')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@carsales.route('/upload',methods = ['GET','POST'])
def upload():
    image = request.files['file']
    if image:
        # Lưu file
        print(image.filename)
        path_to_save = os.path.join(carsales.config['UPLOAD_FOLDER'], image.filename)
        print("Save = ", path_to_save)
        image.save(path_to_save)
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.img (id, url) VALUES (?, ?)", 123, path_to_save)
        conn.commit()
        conn.close()
        return path_to_save # http://server.com/static/path_to_save

    return 'Upload file to detect'


@carsales.route("/img")
def getimg():
    img = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.img")
    for row in cursor.fetchall():
        img.append({"id": row[0], "url": row[1]})
    conn.close()
    return render_template("image.html", img = img)

if(__name__ == "__main__"):
    carsales.run()