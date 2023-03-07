import sqlite3
from sqlite3 import Error
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired

sold_items = {}

class ProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    unit = StringField('unit', validators=[DataRequired()])
    unit_price = FloatField('unit_price', validators=[DataRequired()])

class ProductSaleForm(FlaskForm):
    quantity_to_sale = IntegerField('quantity_to_sale', validators=[DataRequired()])

class Product:
    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    # SELECT
    def all(self):
        #Вибірка списку товарів з бази даних із сортуванням
        conn = self.create_connection("warehouse.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Products ORDER BY Name")     
        rows = cur.fetchall()
        return rows
    
    def allincome(self):
        #Вибірка списку проданих товарів з бази даних із сортуванням
        conn = self.create_connection("warehouse.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Income ORDER BY Name ")     
        rows = cur.fetchall()
        return rows

    #INSERT INTO
    def create(self, data):
        conn = self.create_connection("warehouse.db")
        cur = conn.cursor()
        sql = f"INSERT INTO Products(Name, Quantity, Unit, Unit_Price) VALUES(?,?,?,?)"
        cur.execute(sql, data)
        conn.commit()

    def create_income(self, data):
        conn = self.create_connection("warehouse.db")
        cur = conn.cursor()
        sql = f"INSERT INTO Income(DateIncome, Name, Quantity, Unit, Summ) VALUES(?,?,?,?,?)"
        cur.execute(sql, data)
        conn.commit()

    #UPDATE
    def update(self, id, newquantity):
        conn = self.create_connection("warehouse.db")
        cur = conn.cursor()
        sql = f"UPDATE Products SET Quantity = {newquantity} WHERE id = {id}"
        cur.execute(sql)
        conn.commit()


products = Product()