from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
import re

class Pie:
    DB = "pieshop"

    def __init__(self, data):
        self.id = data["id"]
        self.crust = data["crust"]
        self.topping = data["topping"]
        self.filling = data["filling"]
        self.description = data["description"]
        self.price = data["price"]
        self.image = data["image"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create_pie(cls, data):
        query = """
            INSERT INTO pies (crust, topping, filling, description, price, image)
            VALUES (%(crust)s, %(topping)s, %(filling)s, %(description)s, %(price)s, %(image)s)
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_all_pies(cls):
        all_pies = []
        query = "SELECT * FROM pies;"
        result = connectToMySQL(cls.DB).query_db(query)
        for row in result:
            all_pies.append(cls(row))
        return all_pies
    
    @classmethod
    def get_one_pie(cls, id):
        query = "SELECT * FROM pies WHERE id= %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, id)
        return cls(result[0])
    
    @classmethod
    def update_pie(cls, data):
        query="""
            UPDATE pies
            SET crust = %(crust)s,
                topping = %(topping)s,
                filling = %(filling)s,
                description = %(description)s,
                price = %(price)s,
                image = %(image)s
            WHERE id = %(id)s;
            """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete_pie(cls, id):
        query = "DELETE FROM pies WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,id)

    @staticmethod
    def validate_pie(data):
        valid = True
        if len(data["crust"])<1:
            valid = False
            flash("Please enter a crust", "crust")
        if len(data["topping"])<1:
            valid = False
            flash("Please enter a topping", "topping")
        if len(data["filling"])<1:
            valid = False
            flash("Please enter a filling", "filling")
        if len(data["description"])<5:
            valid = False
            flash("Please enter a breif description", "description")
        if len(data["price"])<1:
            valid = False
            flash("Please enter a filling", "filling")
        return valid