from flask import Flask, render_template, json, redirect, flash
from flask_mysqldb import MySQL
from flask import request
from dotenv import load_dotenv, find_dotenv
import os, re


# Code for the basic structure of this program 
# Date 11/12/2024
# Adapted From 
# Source: https://github.com/osu-cs340-ecampus/flask-starter-app/tree/master

# general config
load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = os.environ.get("340FLASHKEY")

# db config
app.config["MYSQL_HOST"] = os.environ.get("340DBHOST")
app.config["MYSQL_USER"] = os.environ.get("340DBUSER")
app.config["MYSQL_PASSWORD"] = os.environ.get("340DBPW")
app.config["MYSQL_DB"] = os.environ.get("340DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# other global variables
STATES = [
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
        ]

PRICE_PATTERN = r'^\d+(\.\d{1,2})?$'

# routes
@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/products', methods=["POST", "GET"])
def products_page():

    if request.method == "GET":                                                           
        # Queries to populate the products table and dropdowns upon landing on the Products page
        query = "SELECT * FROM Products;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("products.j2", products=data)

    if request.method == "POST":
        cur = mysql.connection.cursor()

        # handler for insert into Products:  
        if request.form.get("add_product"):
            name = request.form["name"].strip()
            model = request.form["model"].strip()
            description = request.form["description"].strip()

            # ensure no duplicates
            query = "SELECT COUNT(*) AS count FROM Products WHERE name = %s  AND model = %s;"
            cur.execute(query, (name, model))
            res = cur.fetchone()["count"]

            # handle case: invalid user input name and model already exist in the table
            if res != 0:                                            
                flash(f"Invalid: Product {name} model {model} already exists. Ensure product Name and Model are unique.", "error")
                return redirect("/products")

            # handle cases: valid and description is or is not null
            if description == "":                           
                query = "INSERT INTO Products (name, model) VALUES (%s, %s);"
                cur.execute(query, (name, model))
            else:                                                  
                query = "INSERT INTO Products (name, model, description) VALUES (%s, %s, %s);"
                cur.execute(query, (name, model, description))

            mysql.connection.commit()
            flash(f"Success: {name} added to Products.", "Success")
            return redirect("/products")
    
        # handler for edit product
        if request.form.get("edit_product"):
            name = request.form["name"].strip()
            model = request.form["model"].strip()

            # Search for productid with name and model pair
            query = "SELECT * FROM Products WHERE name = %s AND model = %s;"
            cur.execute(query, (name, model))
            res = cur.fetchall()

            # Handle case: no product with this name and model pair in the products table.
            if len(res) == 0:
                flash(f"No Such Product: Product {name} model {model} is not found.", "error")
                return redirect("/products")
            
            # Handle case: product 
            else:
                return redirect(f"/edit_product/{res[0]['productId']}")
    
@app.route("/edit_product/<int:productId>", methods=["POST", "GET"])
def edit_product(productId):
    cur = mysql.connection.cursor()
    
    if request.method == "GET":
        # grab values of product with associated productId to display to the user
        query = "SELECT * FROM Products WHERE productId = %s;"
        cur.execute(query, (productId,))
        data = cur.fetchall()

        return render_template("edit_product.j2", product=data)
    
    if request.method == "POST":
        
        if request.form.get("edit_product"):
            # user submits edits
            productId = int(request.form["productId"])
            name = request.form["name"].strip()
            model = request.form["model"].strip()
            description = request.form["description"].strip()

            # ensure no duplicates
            query = "SELECT productId, name, model FROM Products WHERE name = %s AND model = %s;"
            cur.execute(query, (name, model))
            res = cur.fetchall()

            for existing_product in res:
                if existing_product["name"].lower() == name.lower() and existing_product["model"].lower() == model.lower() and existing_product["productId"] != productId:  # is there a product with the same name and model in the table with a different ID? if yes then this is a duplicate.                                  
                    # handle invalid
                    flash(f"Invalid: Product {name} model {model} already exists. Ensure product Name and Model are unique.", "error")
                    return redirect(f"/edit_product/{productId}")
            # handle valid
            if description.strip() == "":                           # Description is NULL
                query = "UPDATE Products SET Products.name = %s, Products.model = %s, Products.description = NULL WHERE Products.productId = %s;"
                cur.execute(query, (name, model, productId))
            else:                                                   # Nothing is NULL
                query = "UPDATE Products SET Products.name = %s, Products.model = %s, Products.description = %s WHERE Products.productId = %s;"
                cur.execute(query, (name, model, description, productId))

            mysql.connection.commit()
            flash(f"Success: {name} has been updated.", "Success")
        return redirect("/products")

@app.route("/delete_product/<int:productId>")
def delete_product(productId):
    # handle deleting the product from the table
    query = "DELETE FROM Products WHERE productId = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (productId,))
    mysql.connection.commit()
    flash(f"Success: product ID: {productId} successfully deleted.", "Success")
    return redirect("/products")

@app.route('/stores', methods=["POST", "GET"])
def stores_page():
    if request.method == "GET":
        # Queries to populate the stores table and dropdowns upon landing on the stores page
        query = "SELECT * FROM Stores;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("stores.j2", stores=data, states=STATES)
    
    if request.method == "POST":
        cur = mysql.connection.cursor()

        # handler for insert into stores: 
        if request.form.get("add_store"):
            name = request.form["name"]
            city = request.form["city"]
            state = request.form["state"]
            streetAddress = request.form["streetAddress"]

            # ensure no duplicates
            query = "SELECT COUNT(*) as count FROM Stores WHERE city = %s AND state = %s AND streetAddress =  %s;" 
            cur.execute(query, (city, state, streetAddress))
            res = cur.fetchone()["count"]

            # handle case: invalid a store at the same location already exists
            if res != 0:
                flash(f"Invalid: A store at {city}, {state}. {streetAddress} already exists. Ensure city, state and street address are unique.", "error")
                return redirect("/stores")     
            # handle case: vaild
            else:    
                query = "INSERT INTO Stores (name, city, state, streetAddress) VALUES (%s, %s, %s, %s);"
                cur.execute(query, (name, city, state, streetAddress))
                mysql.connection.commit()
                flash(f"Success: {name} added to Stores.", "Success")
                return redirect("/stores")

        # handler for edit store
        if request.form.get("edit_store"):
            city = request.form["city"].strip()
            state = request.form["state"].strip()
            streetAddress = request.form["streetAddress"].strip()

            # Search for storeid with name and model pair
            query = "SELECT * FROM Stores WHERE city = %s AND state = %s AND streetAddress = %s;"
            cur.execute(query, (city, state, streetAddress))
            res = cur.fetchall()

            # Handle case: no store at the location specified in the stores table.
            if len(res) == 0:
                flash(f"No Such Store: no store found at {city}, {state}. {streetAddress}", "error")
                return redirect("/stores")
            
            # Handle case: store 
            else:
                return redirect(f"/edit_store/{res[0]['storeId']}")

@app.route("/edit_store/<int:storeId>", methods=["POST", "GET"])
def edit_store(storeId):
    cur = mysql.connection.cursor()
    
    if request.method == "GET":
        # grab values of store with associated storeId to display to the user
        query = "SELECT * FROM Stores WHERE storeId = %s;"
        
        cur.execute(query, (storeId,))
        data = cur.fetchall()

        return render_template("edit_store.j2", store=data, states=STATES)
    
    if request.method == "POST":
        
        if request.form.get("edit_store"):
            # user submits edits
            storeId = int(request.form["storeId"])
            name = request.form["name"].strip()
            city = request.form["city"].strip()
            state = request.form["state"].strip()
            streetAddress = request.form["streetAddress"].strip()

            # ensure no duplicates
            query = "SELECT storeId, city, state, streetAddress FROM Stores WHERE city = %s AND state = %s AND streetAddress = %s;"
            cur.execute(query, ((city, state, streetAddress)))
            res = cur.fetchall()

            for existing_store in res:    # check if a store at this location is already taken to prevent duplicate
                # handle case: duplicate
                if existing_store["city"].lower() == city.lower() and existing_store["state"].lower() == state.lower() and existing_store["streetAddress"].lower() == streetAddress.lower() and existing_store["storeId"] != storeId:                                    
                    flash(f"Invalid: A store at {city}, {state}. {streetAddress} already exists. Ensure city, state and street address are unique.", "error")
                    return redirect(f"/edit_store/{storeId}")
            # handle case: no dulicates                         
            query = "UPDATE Stores SET Stores.name = %s, Stores.city = %s, Stores.state = %s, Stores.streetAddress = %s WHERE Stores.StoreId = %s;"
            cur.execute(query, ((name, city, state, streetAddress, storeId)))
            mysql.connection.commit()
            flash(f"Success: {name} has been updated.", "Success")
            return redirect("/stores")

@app.route("/delete_store/<int:storeId>")
def delete_store(storeId):
    # handle deleting the store from the table
    query = "DELETE FROM Stores WHERE storeId = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (storeId,))
    mysql.connection.commit()
    flash(f"Success: store ID: {storeId} successfully deleted.", "Success")
    return redirect("/stores")   

@app.route('/rewards_customers', methods=["POST", "GET"])
def rewards_customers_page():
    
    # SQL query to populate table from database 
    if request.method == "GET":
        query = "SELECT rewardCustomerID, name, phone, email, address, points FROM Rewards_customers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        return render_template("rewards_customers.j2", rewards_customers = data)
    # Inserts into rewards_customer table when "add_rewards" button is clicked 
    if request.method == "POST":
        if request.form.get("add_rewards"):
           
            name = request.form["name"]
            phone = request.form["pNumber"]
            email = request.form["email"]
            address = request.form["address"]
            points = request.form["points"]


            # Check for duplicate email or phone number
            cur = mysql.connection.cursor()
            query = "SELECT * FROM Rewards_customers WHERE email = %s OR phone = %s"
            cur.execute(query, (email, phone))
            existing_customer = cur.fetchone()
        
      

        if existing_customer:
            # Checks email to make sure it is unique
            if existing_customer["email"] == email:
                flash(f"Invalid: This email is already in use", "error")
                return redirect ("/rewards_customers")
            
            elif existing_customer["phone"] == phone:
                #checks phone number to make sure it is unique
                flash(f"Invalid: This Phone Number is already in use", "error")
                return redirect ("/rewards_customers")
            


            # accounts for null email and address

        else:
            if email == "" and address == "":
                query = "INSERT INTO Rewards_customers (name, phone, points) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, phone, points))
                mysql.connection.commit()
        # accounts for null email
            elif email == "":
                query = "INSERT INTO Rewards_customers (name, phone, address, points) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, phone, address, points))
                mysql.connection.commit()
            # accounts for null address
            elif address == "":
                query = "INSERT INTO Rewards_customers (name, phone, email, points) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, phone, email, points))
                mysql.connection.commit()
    
            # insert if non of the values are null
            else:
                query = "INSERT INTO Rewards_customers (name, phone, email, address, points) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, phone, email, address, points))
                mysql.connection.commit()
        # redirects to rewards_customers once the insert is complete
        flash(f"Success: Customer: {name} successfully created.", "Success")
        return redirect("/rewards_customers")  
    
@app.route("/delete_rewards_customer/<int:rewardCustomerID>", methods=["POST"])
def delete_rewards_customer(rewardCustomerID):
    cur = mysql.connection.cursor()
    query = "DELETE FROM Rewards_customers WHERE rewardCustomerId = %s"
    cur.execute(query, (rewardCustomerID,))
    mysql.connection.commit()
    cur.close()
    flash(f"Success: Customer ID: {rewardCustomerID} successfully deleted.", "Success")
    return redirect("/rewards_customers")

@app.route("/edit_rewards_customer/<int:rewardCustomerID>", methods=["POST", "GET"])
def edit_rewards_customer(rewardCustomerID):
    cur = mysql.connection.cursor()
    
    if request.method == "GET":
        # Selects the customer to edit based on their ID
        query = "SELECT * FROM Rewards_customers WHERE rewardCustomerId = %s;" 
        cur.execute(query, (rewardCustomerID,))
        data = cur.fetchall()

        return render_template("edit_rewards_customers.j2", reward_customer = data)
    
    if request.method == "POST":
        if request.form.get("update_reward"):
            rewardCustomerId = request.form["rewardCustomerId"]
            name = request.form["name"]
            phone = request.form["pNumber"]
            email = request.form["email"]
            address = request.form["address"]
            points = request.form["points"]

            if email == "None" and address == "None":
                query = "UPDATE Rewards_customers SET Rewards_customers.name = %s, Rewards_customers.phone = %s, Rewards_customers.points = %s WHERE Rewards_customers.rewardCustomerId = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, phone, points, rewardCustomerId))
                mysql.connection.commit()
            # accounts for null email
            elif email == "None":
                query = "UPDATE Rewards_customers SET Rewards_customers.name = %s, Rewards_customers.phone = %s,  Rewards_customers.address = %s, Rewards_customers.points = %s WHERE Rewards_customers.rewardCustomerId = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, phone, address, points, rewardCustomerId))
                mysql.connection.commit()
            # accounts for null address
            elif address == "None":
                query = "UPDATE Rewards_customers SET Rewards_customers.name = %s, Rewards_customers.phone = %s, Rewards_customers.email = %s, Rewards_customers.points = %s WHERE Rewards_customers.rewardCustomerId = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, phone, email, points, rewardCustomerId))
                mysql.connection.commit()
            
            else:
                query = "UPDATE Rewards_customers SET Rewards_customers.name = %s, Rewards_customers.phone = %s, Rewards_customers.email = %s, Rewards_customers.address = %s, Rewards_customers.points = %s WHERE Rewards_customers.rewardCustomerId = %s;" 
                cur.execute(query, (name, phone, email, address, points, rewardCustomerId))
                mysql.connection.commit()

            flash(f"Success: Customer ID: {rewardCustomerID} successfully Updated.", "Success")
            return redirect("/rewards_customers")
         
@app.route('/stores_products_details', methods=["POST", "GET"])
def stores_product_details_page():
    if request.method == "GET":
        # Queries to populate the stores_products_details table and dropdowns upon landing on the stores_products_details page   
        query = "SELECT Stores_products_details.storeProductDetailId, Stores.name AS storeName, Stores.city AS city, Stores.state AS state, Stores.streetAddress AS streetAddress, Products.name AS productName, Products.model AS model, Stores_products_details.count, Stores_products_details.price FROM Stores_products_details INNER JOIN Stores ON Stores_products_details.storeId = Stores.storeId INNER JOIN Products ON Stores_products_details.productId = Products.productId;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        query = "SELECT * FROM Stores;"
        cur.execute(query)
        stores = cur.fetchall()
        query = "SELECT productId, name, model FROM Products;"
        cur.execute(query)
        products = cur.fetchall()
        return render_template("stores_products_details.j2", stores_products_details=data, stores=stores, products=products)
    
    if request.method == "POST":
        # handler for insert into stores products details.
        if request.form.get("add_storeProductDetail"):
            storeId = request.form["storeId"]
            productId = request.form["productId"]
            count = request.form["count"].strip()
            price = request.form["price"].strip()

            # perform validation
            cur = mysql.connection.cursor()
            query = "SELECT COUNT(*) AS count FROM Stores_products_details WHERE storeId = %s AND productId = %s;"
            cur.execute(query, (storeId, productId))
            res = cur.fetchone()["count"]

            # ensure no duplicates
            if res != 0:
                # handle case: duplicates
                flash(f"Invalid: Duplicate this product model is already present at this store. Ensure the product is not yet in in the store", "error")
                return redirect("/stores_products_details")
            
            # ensure price is formatted and positive
            elif not re.match(PRICE_PATTERN, price):
                # handle case: price is invalid
                flash(f"Invalid: price format invalid. Ensure format xxx.xx (ex 100.10) and positive", "error")
                return redirect("/stores_products_details")
            
            # ensure count is valid
            elif not count.isdigit():
                # handle case count is invalid
                flash(f"Invalid: count must be whole number", "error")
                return redirect("/stores_products_details")
            # ensure count is positive
            elif not int(count) >= 0:
                # handle case where count is not positive
                flash(f"Invalid: count must not be negative", "error")
                return redirect("/stores_products_details")
            
            # handle case: valid input
            else:
                query = "INSERT INTO Stores_products_details (storeId, productId, count, price) VALUES (%s, %s, %s, %s);"
                cur.execute(query, (storeId, productId, count, price))
                mysql.connection.commit()
                flash("Success: Product added to Store")
                return redirect("/stores_products_details")
            
@app.route("/edit_store_product_detail/<int:storeProductDetailId>", methods=["POST", "GET"])
def edit_store_product_detail(storeProductDetailId):
    cur = mysql.connection.cursor()

    if request.method == "GET":
        # grab values associated with storeProductDetailId to display to the user
        query = "SELECT Stores_products_details.storeProductDetailId, Stores.name AS storeName, Stores.city AS city, Stores.state AS state, Stores.streetAddress AS streetAddress, Products.name AS productName, Products.model AS model, Stores_products_details.count, Stores_products_details.price FROM Stores_products_details INNER JOIN Stores ON Stores_products_details.storeId = Stores.storeId INNER JOIN Products ON Stores_products_details.productId = Products.productId WHERE Stores_products_details.storeProductDetailId = %s;"
        cur.execute(query, (storeProductDetailId,))
        data = cur.fetchall()
        return render_template("edit_store_product_detail.j2", store_product_detail=data)
    
    if request.method == "POST":
        # user submits edits
        if request.form.get("edit_store_product_detail"):
            storeProductDetailId = request.form["storeProductDetailId"]
            count = request.form["count"].strip()
            price = request.form["price"].strip()

            # ensure price is formatted and positive
            if not re.match(PRICE_PATTERN, price):
                # handle case: price is invalid
                flash(f"Invalid: price format invalid. Ensure format xxx.xx (ex 100.10) and positive", "error")
                return redirect("/stores_products_details")
            
            # ensure count is valid
            elif not count.isdigit():
                # handle case count is invalid
                flash(f"Invalid: count must be whole number", "error")
                return redirect("/stores_products_details")
            # ensure count is positive
            elif not int(count) >= 0:
                # handle case where count is not positive
                flash(f"Invalid: count must not be negative", "error")
                return redirect("/stores_products_details")
            
            # handle valid input
            else:
                query = "UPDATE Stores_products_details SET Stores_products_details.count = %s, Stores_products_details.price = %s WHERE Stores_products_details.storeProductDetailId = %s;"
                cur.execute(query, (count, price, storeProductDetailId))
                mysql.connection.commit()
                flash(f"Success: Edits were applied.", "Success")
                return redirect("/stores_products_details")

@app.route("/delete_store_product_detail/<int:storeProductDetailId>")
def delete_store_product_detail(storeProductDetailId):
    query = "DELETE FROM Stores_products_details WHERE storeProductDetailId = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (storeProductDetailId,))
    mysql.connection.commit()
    flash(f"Success: storeProductDetailID: {storeProductDetailId} successfully deleted.", "Success")
    return redirect("/stores_products_details")
            
@app.route('/sales_transactions', methods = ["POST", "GET"])
def sales_transactions_page():
    cur = mysql.connection.cursor()
    if request.method == "GET":
        # Fills transaction table with data from Sales_transactions
        query = """SELECT 
        Sales_transactions.saleTransactionId, 
        Stores.name AS storeName, 
        Sales_transactions.date, 
        Rewards_customers.name AS rewardCustomerName, 
        Sales_transactions.total, 
        Sales_transactions.pointsApplied, 
    ROUND 
        (Sales_transactions.total - (Sales_transactions.pointsApplied / 100), 2) AS finalAmount
    FROM 
        Sales_transactions
    LEFT JOIN 
        Stores 
    ON 
        Sales_transactions.storeId = Stores.storeId
    LEFT JOIN 
        Rewards_customers 
    ON 
        Sales_transactions.rewardCustomerId = Rewards_customers.rewardCustomerId;"""
        
        cur.execute(query)
        data = cur.fetchall()
        # Selects stores for dropdown menu
        query = "SELECT * FROM Stores;"
        cur.execute(query)
        stores = cur.fetchall()
        # Selects Rewards Customer for dropdown menu
        query = "SELECT * FROM Rewards_customers;"
        cur.execute(query)
        customers = cur.fetchall()

        return render_template("sales_transactions.j2", sales_transactions=data, stores = stores, customers = customers)
    
    if request.method == "POST":
        
        if request.form.get("add_transaction"):
            cur = mysql.connection.cursor()
            storeId = request.form["storeId"]
            date = request.form["date"]
            rewardCustomerId = request.form["rewardCustomerId"]
            total = float(request.form["total"])
            pointsApplied = int(request.form["points"]) if request.form["points"] else 0 
            # Calculates the total price by subrating $1 for every 100 points
            finalAmount = round(total - (pointsApplied / 100), 2)
            # Makes sure a rewards customer is selected in oreder to use points 
            if rewardCustomerId == "" and pointsApplied != "" or 0:
                flash(f"Invalid: Points cannot be applied if no customer is selected", "error")
                return redirect("/sales_transactions")
            # Makes sure value of points applied is greater than 0
            if pointsApplied < 0:
                flash(f"Invalid: points applied must be positive number", "error")
                return redirect("/sales_transactions")
            # Makes sure price is greater than 0
            if total < 0:
                flash(f"Invalid: Total applied must be positive number", "error")
                return redirect("/sales_transactions")
            



            
            
            if rewardCustomerId == "" and pointsApplied == "":
                query = "INSERT INTO Sales_transactions (storeId, date, total, finalAmount) VALUES (%s, %s, %s, %s);"
                cur.execute(query, (storeId, date, total, finalAmount))
                mysql.connection.commit()
            
            elif rewardCustomerId == "":
                query = "INSERT INTO Sales_transactions (storeId, date, total, pointsApplied, finalAmount) VALUES (%s, %s, %s, %s, %s);"
                cur.execute(query, (storeId, date, total, pointsApplied, finalAmount))
                mysql.connection.commit()

                

            
            elif pointsApplied == "":
                query = "INSERT INTO Sales_transactions (storeId, date, RewardCustomerId, total, finalAmount) VALUES (%s, %s, %s, %s, %s);"
                cur.execute(query, (storeId, date, rewardCustomerId, total, finalAmount))
                mysql.connection.commit()
            
            else:
                query = "INSERT INTO Sales_transactions (storeId, date, RewardCustomerId, total, pointsApplied, finalAmount) VALUES (%s, %s, %s, %s, %s, %s);"
                cur.execute(query, (storeId, date, rewardCustomerId, total, pointsApplied, finalAmount))
                mysql.connection.commit()
                
        flash(f"Success: Sale Transaction Added", "success")
        return redirect("/sales_transactions")
        
@app.route('/sales_transactions_details', methods = ["POST", "GET"])
def sales_transactions_details_page():
    cur = mysql.connection.cursor()
    if request.method == "GET":
        # populates table 
        query = """SELECT 
            Sales_transactions_details.saleTransactionDetailId, 
            Sales_transactions_details.saleTransactionId, 
            Products.name as productName, 
            Sales_transactions_details.quantity, 
            Sales_transactions_details.total 
            
        FROM 
            Sales_transactions_details 
        LEFT JOIN 
            Products 
        ON 
            Sales_transactions_details.productId = Products.productId;"""
        cur.execute(query)
        data = cur.fetchall()
        # Selects products to populate dropdown menu
        query = "SELECT * FROM Products;"
        cur.execute(query)
        products = cur.fetchall()
        # Select Transaction ID 
        query = "SELECT * FROM Sales_transactions"
        cur.execute(query)
        transactions = cur.fetchall()
        return render_template("sales_transactions_details.j2", sales_transactions_details=data, products=products, transactions = transactions)  

    if request.method == "POST":
        if request.form.get("add_transaction_details"):
            cur = mysql.connection.cursor()
            saleTransactionId = request.form["saleTransactionId"]
            productId = request.form["productId"]
            quantity = request.form["quantity"]
            total = request.form["total"]
            # Makes sure all feilds are filled even though required in html
            if not saleTransactionId or not productId or not quantity or not total:
                flash("All fields are required.", "error")
                return redirect("/sales_transactions_details")
            # makes sure total matches given price pattern and is positive 
            if not re.match(PRICE_PATTERN, total):
                flash(f"Invalid: price format invalid. Ensure format xxx.xx (ex 100.10) and positive", "error")
                return redirect("/sales_transactions_details")
            # makes sure total is positive 
            if not float(total) >= 0:
                flash(f"Invalid: Total must not be negative", "error")
                return redirect("/sales_transactions_details")
            # makes sure quantity is a whole number and is not negative
            if not quantity.isdigit():
                flash(f"Invalid: quantity must be positive whole number", "error")
                return redirect("/sales_transactions_details")
           
            

           # inserts transaction details into table and shows success message 
            query = "INSERT INTO Sales_transactions_details (saleTransactionId, productId, quantity, total) VALUES (%s, %s, %s, %s);"
            cur.execute(query, (saleTransactionId, productId, quantity, total))
            mysql.connection.commit()

        flash(f"Success: Sale Transaction Details Added", "success")
        return redirect("/sales_transactions_details")
  
# For Production: gunicorn -b 0.0.0.0:20868 app:app --timeout 120
#       add -D for background daemone
# For production and debugging: gunicorn -b 0.0.0.0:20868 app:app --timeout 120 --log-level debug
# To kill a gunicor processes for a user: pkill -u <userNameHere> gunicorn
# listener: 
if __name__ == "__main__":
    app.run()