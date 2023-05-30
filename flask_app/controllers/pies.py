from flask_app import app
from flask import render_template, redirect, session, request, flash
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
    session['open_cart'] = False
    session['open_login'] = False
    session['open_register'] = False
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
        img_to_upload = request.files["image"]
        user_id = session["user_id"]
        data = {
            "crust":request.form["crust"],
            "topping":request.form["topping"],
            "filling":request.form["filling"],
            "description":request.form["description"],
            "price":request.form["price"],
        }
        res = cloudinary.uploader.upload(img_to_upload, folder="pyshop", public_id=data["filling"],unique_filename=False, overwrite=True)
        img_url = res["secure_url"]
        data["image"] = img_url
        pie.Pie.create_pie(data)
        session.clear()
        session["user_id"] = user_id
        return redirect("/menu")

@app.route("/pies/delete/<int:id>")
def delete_pie(id):
    if "user_id" in session and session["user_id"] < 3:
        res = pie.Pie.get_img_to_delete({"id":id})
        print(res)
        img_url=res["image"]
        cloudinary.uploader.destroy(img_url)
        pie.Pie.delete_pie({"id":id})
        return redirect('/menu')
    return redirect("/menu")

@app.route("/add_to_cart/<filling>/<float:price>/<int:id>", methods=["POST"])
def add_to_cart(filling, price, id):
    if "cart" not in session:
        cart=[]
    else:
        cart= session["cart"]
    
    parse_pie={
        "id":id,
        "filling":filling,

        "price":price,
        "quantity":int(request.form["quantity"])
    }

    if not any(_pie["filling"] == parse_pie["filling"] for _pie in cart):
        cart.append(parse_pie)
    else:
        for pie in cart:
            if pie["filling"] == parse_pie["filling"]:
                pie["quantity"] += parse_pie["quantity"]
                break

    subtotal = 0
    for pie in cart:
        subtotal += (pie["price"] * pie["quantity"])

    session["cart"] = cart
    session["subtotal"] = subtotal

    flash(f"{parse_pie['quantity']} {parse_pie['filling']} pie(s) were added to cart", "cart_update")
    print(f"{cart}")
    return redirect("/menu")

@app.route("/remove_from_cart/<int:id>")
def remove_from_cart(id):
    cart = session['cart']
    # for i in range(len(session['cart'])):
    #     print(type(session['cart'][i]['id']))
    #     print(type(id))
    #     if session['cart'][i]['id'] == id:
    #         print('match!')
    #         cart.pop(i)
    #         break
    cart[:] = [x for x in cart if x.get('id') != id]
    subtotal = 0
    for item in cart:
        subtotal += (item["price"] * item["quantity"])
    session["subtotal"] = subtotal
    session['open_cart'] = True
    menu = pie.Pie.get_all_pies()
    return render_template("menu.html", menu=menu)