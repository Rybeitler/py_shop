from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import user

@app.route('/')
def index():
    if "user_id" in session:
        return redirect('/')
    return render_template("index.html")

@app.route('/register', methods=["POST"])
def register():
    if not user.User.validate_register(request.form):
        for key in request.form:
            session[key] = request.form[key] 
        return redirect('/')
    user_id = user.User.register(request.form)
    session.clear()
    session['user_id'] = user_id
    return redirect('/')