from flask import Flask, flash, render_template, url_for, request, redirect, session
from pymongo import MongoClient
from bson.json_util import dumps
from random import randint

# pw - ygZA8rwryIEeHGJt

client = MongoClient("mongodb+srv://Daniils:ygZA8rwryIEeHGJt@preject.9gy7x.mongodb.net/Preject?retryWrites=true&w=majority")

db = client.Preject
users_db = db.users

db = client.Preject
product_db = db.product

app = Flask(__name__)
app.secret_key = "hkIbg#45f1_"



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

#log in funkcija
@app.route('/auth/login', methods=["GET","POST"])
def login():
    if "auth" in session:
        return render_template("home.html")
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            a = users_db.find_one({"username":username})
            b = users_db.find_one({"username":username},{"password":password})

            if a != None or b != None:
                a = a['username']
                b = b['password']

            if a != username or b != password:
                return render_template("login.html")

            session["auth"] = username

            return redirect(url_for("home"))

        else:
            return render_template("login.html")

@app.route('/auth/reset')
def recovery():
    return render_template('reset.html')

#reģistrācija
@app.route('/auth/register', methods=["GET","POST"])
def register():
    if "auth" in session:
        return redirect(url_for("home"))
    else:
        if request.method == 'POST':
            id_ = randint(100,10000000)

            email = request.form['email']
            username = request.form['username']
            password = request.form['password']

            a = users_db.find_one({"email":email})
            if a != None:
                a = a['email']

            if a == email:
                return render_template("register.html")

            session["auth"] = username

            users_db.insert_one({"id":id_,"email":email,"username":username,"password":password,})
            return redirect(url_for("home"))
        else:
            return render_template("register.html")

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/findproduct')
def findproduct():
    return render_template('findproduct.html')

#jaunu preci pievienošana
@app.route('/panel', methods=["GET","POST"])
def panel():
    if "auth" in session:
        if session["auth"] == "admin":
            session["auth"] = 'admin'
            if request.method == 'POST':
                id_ = randint(100,10000000)

                cost = request.form['cost']
                model = request.form['model']
                prcategory = request.form['prcategory']
                img = request.form['img']

                a = product_db.find_one({"model":model})

                if a != None:
                    a = a['model']
            
                if a == model:
                    return render_template("panel.html")
            
                session["auth"] = "admin"

                if cost == "" or model == "" or prcategory == "" or img == "":
                    return render_template('panel.html')
                else:
                    product_db.insert_one({"id":id_,"cost":cost,"model":model,"prcategory":prcategory,"img":img})
                    return render_template('panel.html')
            else:
                return render_template('panel.html') 
        else:
            return render_template('home.html')

#ja lietotājs ir 'admin' tiek dota admina daļa
@app.route('/findproduct/phones')
def phones():
    if "auth" in session:
        if session["auth"] == "admin":
            session["auth"] = 'admin'
            return render_template('phonesadmin.html')  
        else:
            return render_template('phones.html')

#produktu dzēšana        
@app.route("/panel/delete/<int:id_>", methods=["GET","POST"])
def delete(id_):
    if "auth" in session:
        if session["auth"] == "admin":
            product_db.delete_one({"id":id_})
            return redirect(url_for("panel"))
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

#ja lietotājs ir 'admin' tiek dota admina daļa
@app.route('/findproduct/computer')
def computer():
    if "auth" in session:
        if session["auth"] == "admin":
            session["auth"] = 'admin'
            return render_template('computeradmin.html')  
        else:
            return render_template('computer.html')


@app.route('/editprof')
def editprof():
    return render_template('profileedit.html')

@app.route('/profile', methods=["GET", "POST"] )
def profile():
    return render_template('profile.html')

@app.route('/card')
def card():
    return render_template('card.html')

#log out funkcija
@app.route('/logout', methods=["GET","POST"])
def logout():
    session.pop("auth", None)
    return redirect(url_for("home"))

@app.route('/data')
def data():
    product = product_db.find()
    data = list(product)
    return dumps(data)

@app.route("/findproduct/phones/buy/<int:id>", methods=["GET","POST"])
def buy(id):
    id_ = id
    product_database = product_db.find_one({"id":id_})
    if 'auth' in session:
        user = session['auth']
        users_db.update_one({"username":user}, {"$set": {"buy":id_}})
        product = product_database['model']
        cena = product_database['cost']
        return render_template('check.html', user=user, id=id_, product=product, cena=cena)
    else:
        return redirect(url_for("home"))


#darbība no Mārisa video
@app.route('/users')
def users():
    users_data = users_db.find()
    if users_data:
        return dumps(users_data)
    else:
        return {"error":"No users in DB"}


@app.route('/user/<id>')
def user(id):
    user = users_db.find_one({"_id":ObjectId(id)})
    if user:
        return dumps(user)
    else:
        return {"error":"User not found"}

@app.route('/user/create', methods = ['POST'])
def createUser():
    if request.method == 'POST' and request.content_type == 'application/json':
        dati = request.json
        users_db.insert_one({"vards":dati['vards'], "uzvards":dati['uzvards'], "status":dati['status']})
        return {"message":"User created!"}
    else:
        return {"error":"Method or content type not supported!"}


app.run(host='0.0.0.0', port=80, debug=True)