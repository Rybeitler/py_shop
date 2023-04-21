from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import user, pie

import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
load_dotenv()

@app.route('/menu')
def menu():
    # if "user_id" in session:
    #     user_data = user.User.get_user_by_id(session["user_id"])
    menu = pie.Pie.get_all_pies()
    return render_template("menu.html", menu=menu)

@app.route("/pies/create")
def create_pie():
    if "user_id" not in session:
        return redirect("/")
    return render_template("add_pie.html")



@app.route('/pies/add', methods=["POST"])
def add_pie():
    if "user_id" not in session:
        return redirect('/')
    if not pie.Pie.validate_pie(request.form):
        session["crust"] = request.form["crust"]
        session["topping"] = request.form["topping"]
        session["filling"] = request.form["filling"]
        session["description"] = request.form["description"]
        session["price"] = request.form["price"]
        return redirect("/pies/create")
    else:
        print('here')
        img_to_upload = request.files["image"]
        user_id = session["user_id"]
        data = {
            "crust":request.form["crust"],
            "topping":request.form["topping"],
            "filling":request.form["filling"],
            "description":request.form["description"],
            "price":request.form["price"],
        }
        cloudinary.uploader.upload(img_to_upload, folder="pyshop", public_id=data["filling"],unique_filename=False, overwrite=True)
        img_url = cloudinary.CloudinaryImage(data["filling"]).build_url()
        data["image"] = img_url
        pie.Pie.create_pie(data)
        session.clear()
        session["user_id"] = user_id
        return redirect("/menu")
        
    