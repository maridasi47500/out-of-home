from flask import Flask, render_template, request, session, redirect
from myplace import Myplace
from bs4 import BeautifulSoup
import subprocess
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,password,email,phone,country_id) values (:username,:password,:email,:phone,:country_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from user')


        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','password','email','phone','country_id']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','password','email','phone','country_id']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','password','email','phone','country_id']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_city", methods=["GET","POST"])
def add_one_city():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into city (name,country_id) values (:name,:country_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from city')


        return render_template("cityform.html", citys=user, one_user=one_user, the_title="add new city", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from city')
    one_user = query_db("select * from city limit 1", one=True)
    return render_template("cityform.html", citys=user, one_user=one_user, the_title="add new city", touslescountry=touslescountry)

@app.route("/add_one_userhasarrival", methods=["GET","POST"])
def add_one_userhasarrival():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescity= query_db("select * from city")

        one_user = query_db("insert into userhasarrival (city_id,user_id) values (:city_id,:user_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from userhasarrival')


        return render_template("userhasarrivalform.html", userhasarrivals=user, one_user=one_user, the_title="add new userhasarrival", touslescity=touslescity)


    touslescity= query_db("select * from city")

    user = query_db('select * from userhasarrival')
    one_user = query_db("select * from userhasarrival limit 1", one=True)
    return render_template("userhasarrivalform.html", userhasarrivals=user, one_user=one_user, the_title="add new userhasarrival", touslescity=touslescity)

@app.route("/add_one_oohads", methods=["GET","POST"])
def add_one_oohads():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        touslescity= query_db("select * from city")

        one_user = query_db("insert into oohads (city_id,pic,user_id,message) values (:city_id,:pic,:user_id,:message)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from oohads')


        return render_template("oohadsform.html", oohadss=user, one_user=one_user, the_title="add new oohads", touslescity=touslescity)


    touslescity= query_db("select * from city")

    user = query_db('select * from oohads')
    one_user = query_db("select * from oohads limit 1", one=True)
    return render_template("oohadsform.html", oohadss=user, one_user=one_user, the_title="add new oohads", touslescity=touslescity)

@app.route("/add_one_lyricsongs", methods=["GET","POST"])
def add_one_lyricsongs():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into lyricsongs (city_id,lyrics,user_id) values (:city_id,:lyrics,:user_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from lyricsongs')


        return render_template("lyricsongsform.html", lyricsongss=user, one_user=one_user, the_title="add new lyricsongs")


    user = query_db('select * from lyricsongs')
    one_user = query_db("select * from lyricsongs limit 1", one=True)
    return render_template("lyricsongsform.html", lyricsongss=user, one_user=one_user, the_title="add new lyricsongs")

@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from country')


        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

