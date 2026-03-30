from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO
from pymongo import MongoClient
from werkzeug.utils import secure_filename
client = MongoClient(
    'mongodb+srv://shilham:shilhama5@cluster0.v0kxevt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbhair

import jwt
import datetime
from bson import ObjectId

app = Flask(__name__)
socketio = SocketIO(app)

SECRET_KEY = "AFIVEHAIR"

@app.route('/')
def home():
    token_receive = request.cookies.get("mytoken")
    articles = list(db.articles.find({}, {'_id': False}))
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["username"]})
        status = user_info['status']
        return render_template("dashboard.html", status = status, user_info = user_info, articles = articles, page="dashboard")
    except jwt.ExpiredSignatureError:
        return render_template("articles.html", status="guest", articles = articles, page="article")
    except jwt.exceptions.DecodeError:
        return render_template("articles.html", status="guest", articles = articles, page="article")


@app.route('/articles')
def articles():
    token_receive = request.cookies.get("mytoken")
    articles = list(db.articles.find({}, {'_id': False}))
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["username"]})
        status = user_info['status']
        return render_template("articles.html", status = status, user_info = user_info, articles = articles, page="article")
    except jwt.ExpiredSignatureError:
        return render_template("articles.html", status="guest", articles = articles, page="article")
    except jwt.exceptions.DecodeError:
        return render_template("articles.html", status="guest", articles = articles, page="article")


@app.route('/articles/<id_article>')
def article_content(id_article):
    article = db.articles.find_one({'article_id': id_article}, {'_id': False})
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["username"]})
        status = user_info['status']
        return render_template('article_content.html', article=article, status = status, user_info = user_info, page="article")
    except jwt.ExpiredSignatureError:
        return render_template('article_content.html', article=article, status="guest", page="article")
    except jwt.exceptions.DecodeError:
        return render_template('article_content.html', article=article, status="guest", page="article")


@app.route('/get_articles')
def get_articles():
    articles = list(db.articles.find({}, {'_id': False}))
    return jsonify({
        'result': 'success',
        'articles': articles
    })


@app.route('/articles/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        article_id = request.form["article_id"]
        title = request.form["title"]
        desc = request.form["desc"]
        first_p = request.form["first_p"]
        second_p = request.form["second_p"]
        third_p = request.form["third_p"]
        new_doc = {
            'article_id': article_id,
            'title': title,
            'description': desc,
            'first_p': first_p,
            'second_p': second_p,
            'third_p': third_p
        }
        file = request.files["article_img"]
        filename = secure_filename(file.filename)
        extension = filename.split(".")[-1]
        file_path = f"article_img/{article_id}.{extension}"
        file.save("./static/" + file_path)
        new_doc["article_img"] = filename
        new_doc["article_img_real"] = file_path
        db.articles.insert_one(new_doc)
        return jsonify({"result": "success", "msg": "Article Added!"})
    token_receive = request.cookies.get("mytoken")
    articles = list(db.articles.find({}, {'_id': False}))
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["username"]})
        status = user_info['status']
        return render_template('create_articles.html', status = status, user_info = user_info, page="article")
    except jwt.ExpiredSignatureError:
        return redirect(url_for('home'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('home'))
    


@app.route('/articles/edit/<id_article>')
def article_edit(id_article):
    token_receive = request.cookies.get("mytoken")
    articles = list(db.articles.find({}, {'_id': False}))
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["username"]})
        status = user_info['status']
        article = db.articles.find_one({'article_id': id_article}, {'_id': False})
        return render_template('edit_articles.html', article=article, status = status, user_info = user_info, page="article")
    except jwt.ExpiredSignatureError:
        return redirect(url_for('home'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('home'))
    

@app.route('/articles/edit', methods=['POST'])
def edit_article():
    article_id = request.form["article_id"]
    title = request.form["title"]
    desc = request.form["desc"]
    first_p = request.form["first_p"]
    second_p = request.form["second_p"]
    third_p = request.form["third_p"]
    new_doc = {
        'article_id': article_id,
        'title': title,
        'description': desc,
        'first_p': first_p,
        'second_p': second_p,
        'third_p': third_p
    }
    if "article_img" in request.files:
        file = request.files["article_img"]
        filename = secure_filename(file.filename)
        extension = filename.split(".")[-1]
        file_path = f"article_img/{article_id}.{extension}"
        file.save("./static/" + file_path)
        new_doc["article_img"] = filename
        new_doc["article_img_real"] = file_path
    db.articles.update_one({"article_id": article_id}, {"$set": new_doc})
    return jsonify({"result": "success", "msg": "Article Updated!"})

@app.route('/articles/delete', methods=['POST'])
def delete_article():
    article_id = request.form["article_id"]
    db.articles.delete_one({"article_id" : article_id})
    return jsonify({
        "result": "success"
    })

@app.route('/booking')
def booking():
    token_receive = request.cookies.get("mytoken")
    articles = list(db.articles.find({}, {'_id': False}))
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["username"]})
        status = user_info['status']
        if status == 'user':
            booking = list(db.booking.find({"username": payload["username"]}))
        else:
            booking = list(db.booking.find({}))
        return render_template("booking.html", status = status, user_info = user_info, booking = booking, page="booking")
    except jwt.ExpiredSignatureError:
        return redirect(url_for('home'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('home'))
    
@app.route('/booking/create', methods=['GET', 'POST'])
def create_booking():
    if request.method == 'POST':
        username = request.form["username"]
        title = request.form["title"]
        date = request.form["date"]
        hour = request.form["hour"]
        hairtype = request.form["hairtype"]
        hairstylist = request.form["hairstylist"]
        new_doc = {
            'username': username,
            'title': title,
            'date': date,
            'hour' : hour,
            'hairtype':  hairtype,
            'hairstylist': hairstylist,
            'status' : 'Pending'
        }
        db.booking.insert_one(new_doc)
        return jsonify({"result": "success", "msg": "You've made an appointment!"})
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["username"]})
        hairstylists = db.users.find({"status" : "admin"})
        status = user_info['status']
        return render_template('create_booking.html', status = status, user_info = user_info, page="booking", hairstylists=hairstylists)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('home'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('home'))

@app.route('/booking/approve', methods=['POST'])
def approve_booking():
    booking_id = request.form["booking_id"]
    db.booking.update_one({"_id" : ObjectId(booking_id)}, {'$set' : {'status' : 'Approved'}})
    return jsonify({
        "result": "success"
    })

@app.route('/booking/deny', methods=['POST'])
def deny_booking():
    booking_id = request.form["booking_id"]
    db.booking.update_one({"_id" : ObjectId(booking_id)}, {'$set' : {'status' : 'Denied'}})
    return jsonify({
        "result": "success"
    })

@app.route('/booking/delete', methods=['POST'])
def delete_booking():
    booking_id = request.form["booking_id"]
    db.booking.delete_one({"_id" : ObjectId(booking_id)})
    return jsonify({
        "result": "success"
    })

@app.route('/consultation')
def consultation():
    token_receive = request.cookies.get("mytoken")
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
    user_info = db.users.find_one({"username": payload["username"]})
    status = user_info['status']
    if status == 'user':
            consult = list(db.consultation.find({"username": payload["username"]}))
    else:
            consult = list(db.consultation.find({}))
    return render_template('consultation.html', page='consultation', status=status, user_info=user_info, consults=consult)

@app.route('/consultation/create', methods=['GET', 'POST'])
def create_consult():
    if request.method == 'POST':
        username = request.form["username"]
        consultation_id = request.form["consult_id"]
        if db.consultation.find_one({'consultation_id': consultation_id}):
            return jsonify({'result': 'exist_consult'})
        consultation_title = request.form["consult_title"]
        new_doc = {
            'consultation_id': consultation_id,
            'consultation_title': consultation_title,
            'username' : username,
        }
        db.consultation.insert_one(new_doc)
        return jsonify({"result": "success"})
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["username"]})
        status = user_info['status']
        return render_template('create_consult.html', status = status, user_info = user_info, page="consultation")
    except jwt.ExpiredSignatureError:
        return redirect(url_for('home'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('home'))

@app.route('/consultation/<consult_id>')
def consult_chat(consult_id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["username"]})
        status = user_info['status']
        messages = db.messages.find({'consult_id' : consult_id})
        cons = db.consultation.find_one({'consultation_id' : consult_id})
        return render_template('consult_chat.html', status = status, user_info = user_info, messages=messages, page="consultation", cons_id = consult_id, cons=cons)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('home'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('home'))
    
@socketio.on('chat_message')
def handle_message(data):
    time_now = datetime.datetime.now()
    timestamp = time_now.timestamp()
    db.messages.insert_one(
        {'consult_id' : data['consult_id'],
         'sender': data['sender'], 
         'message': data['message'],
         'timestamp' : timestamp
         })
    socketio.emit('chat_message', data)

@app.route('/consultation/delete', methods=['POST'])
def delete_consultation():
    consult_id = request.form["consult_id"]
    db.messages.delete_many({"consult_id" : consult_id})
    db.consultation.delete_one({"consultation_id" : consult_id})
    
    return jsonify({
        "result": "success"
    })


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username_receive']
        email = request.form['email_receive']
        password = request.form['password_receive']
        status = 'user'

        if db.users.find_one({'username': username}):
            return jsonify({
                'result': 'exist_username'
            })

        if db.users.find_one({'email': email}):
            return jsonify({
                'result': 'exist_email'
            })

        user = {
            'username': username,
            'email': email,
            'password': password,
            'status' : status
        }
        db.users.insert_one(user)
        return jsonify({
            'result': 'success'
        })

    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username_receive')
        password = request.form.get('password_receive')

        user_password = db.users.find_one(
            {'$or': [{'username': username}, {'email': username}]}, {'_id': False})
        
        if user_password:
            if password == user_password['password']:
                my_username = user_password['username']
                my_status = user_password['status']
                payload = {
                "username": my_username,
                "status": my_status,
                "exp": datetime.datetime.now(datetime.UTC)+ datetime.timedelta(hours=5),
                }
                token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
                return jsonify({"result": "success", "token": token})

    return render_template('login.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
    
