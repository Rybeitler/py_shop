from flask import Flask, flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$")



class User:
    DB = "pieshop"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register(cls, user_data):
        data = {
            "first_name":user_data["first_name"],
            "last_name":user_data["last_name"],
            "email":user_data["email"],
            "password":bcrypt.generate_password_hash(user_data["password"])
        }
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_user_by_id(cls, id):
        data = {
            "id":id
            }
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        print(f"{result} id")
        return cls(result[0])

    @classmethod
    def get_user_by_email(cls, email):
        data = {
            "email":email
            }
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        print(f"{result} email")
        if len(result) ==0:
            return False
        else:
            return cls(result[0])

    @staticmethod
    def validate_register(data):
        valid = True
        if len(data['first_name']) < 3:
            flash("Please enter a first name longer than 3 characters", "first_name")
            valid = False
        if len(data['last_name']) < 3:
            flash("Please enter a last name longer than 3 characters", "last_name")
            valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email format', "email")
            valid = False
        if User.get_user_by_email(data['email']):
            flash('Email is already in use', "email")
            valid = False
        if not PW_REGEX.match(data["password"]):
            valid = False
            flash("Passwords must be at least 8 characters and contain one capital and one number", "password")
        if data['password'] != data['confirm_password'] :
            flash('Passwords do not match', "confirm_password")
            valid = False
        return valid