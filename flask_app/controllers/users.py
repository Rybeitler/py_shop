from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import user

@app.route('/')
def index():
    # if "user_id" in session:
    session['open_cart'] = False
    session['open_login'] = False
    session['open_register'] = False
    return render_template("home.html")




@app.route('/register', methods=["POST"])
def register():
    if not user.User.validate_register(request.form):
        for key in request.form:
            session[key] = request.form[key] 
        session["open_register"] = True
        return render_template("home.html")
    user_id = user.User.register(request.form)
    logged_in_user = user.User.get_user_by_id(user_id)
    session.clear()
    session['user_id'] = user_id
    session['first_name'] = logged_in_user
    return redirect('/')

@app.route('/login', methods=["Post"])
def login():
    logged_in_user = user.User.validate_login(request.form)
    if not logged_in_user:
        for key in request.form:
            session[key] = request.form[key]
        session["open_login"] = True
        return render_template("home.html")
    else:
        session.clear()
        session["user_id"] = logged_in_user.id
        session["first_name"] = logged_in_user.first_name
        return redirect('/')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")