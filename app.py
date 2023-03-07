import datetime
from flask import Flask, jsonify, abort, make_response, request, render_template
from models import products
from models import sold_items

app = Flask(__name__)
app.config["SECRET_KEY"] = "warehouse"

product_items = {}


@app.route('/', methods=["GET"])
def homepage():   
    return render_template("base.html")

@app.route('/listproducts', methods=["GET"])
def product_list():
    items = products.all()
    return render_template("product_list.html", items=items)

@app.route('/addproduct', methods=["POST"])
def product_add():
    data = request.form  
    name = data.get('name')
    quantity = data.get('quantity')
    unit = data.get('unit')
    unit_price = data.get('unit_price')
    product = (name, quantity, unit, unit_price)
    products.create(product)
    items = products.all()
    return render_template("product_list.html", items=items)

@app.route('/sell/<product_name>', methods=["POST"])
def sell_product(product_name):
    product_items = products.all()
    for product_item in product_items:
        if product_item[1] == product_name:
            result_quantity = int(product_item[2])
            result_index = int(product_item[0])
            unit = product_item[3]
            unit_price = float(product_item[4])
    return render_template("sell_product.html", product_name=product_name, 
                                                result_quantity=result_quantity, 
                                                old_quantity=result_quantity,
                                                idproduct=result_index,
                                                unit=unit, 
                                                unit_price=unit_price)

@app.route('/selling/<product_name>', methods=["POST"])
def selling_product(product_name):
    if request.method == "POST": 
        data = request.form
        idproduct = int(data.get('idproduct'))        
        quantity_to_sale = int(data.get('quantity_to_sale'))
        new_quantity = int(data.get('quantity')) - quantity_to_sale
        products.update(idproduct, new_quantity)
        items = products.all()

        #запис у таблицю Income
        today = datetime.date.today().strftime("%d-%m-%Y")
        name = data.get('product_name')
        print(today)
        quantity = quantity_to_sale
        unit = data.get('unit')
        unit_price = data.get('unit_price')
        summ = quantity_to_sale * float(unit_price)
        income = (today, name, quantity, unit, summ)
        products.create_income(income)
    
        return render_template("product_list.html", items=items)

@app.route('/listincome', methods=["GET"])
def income_list():
    items = products.allincome()
    #Вираховування суми
    totalsum = 0
    for item in items:
        totalsum += float(item[4])
    return render_template("income_list.html", items=items, costs=totalsum)
        

if __name__ == '__main__':
    app.run(debug=True)
