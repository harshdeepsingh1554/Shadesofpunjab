# from flask import Flask, render_template, request, redirect ,url_for
# from pymongo import MongoClient

# import datetime
# import os

# app = Flask(__name__)



# try:
#     client = MongoClient("mongodb+srv://harshpocof1:VSrGJdHFCAwFboB4@shades.6c9hcce.mongodb.net/billing?retryWrites=true&w=majority")
#     db = client['billing']
#     bills_collection = db['bills']
#     print("✅ Connected to MongoDB!")
# except Exception as e:
#     print("❌ Connection failed:", e)


# @app.route('/')
# def index():
#     return render_template('index.html')



# @app.route('/add_bill', methods=['POST'])
# def add_bill():
#     customer = request.form['customer']
#     amount = float(request.form['amount'])
#     items = request.form['items']

#     data = {
#         "customer": customer,
#         "amount": amount,
#         "items": items,
#         "date": datetime.datetime.now()
#     }
#     bills_collection.insert_one(data)
    
#     # Redirect to home with query parameters
#     return redirect(url_for('index', success=1, customer=customer, amount=amount))





# @app.route('/bills')
# def view_bills():
#     bills = list(bills_collection.find())
#     return render_template('bills.html', bills=bills)

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import datetime
import os

app = Flask(__name__)

# MongoDB connection
try:
    client = MongoClient("mongodb+srv://harshpocof1:VSrGJdHFCAwFboB4@shades.6c9hcce.mongodb.net/billing?retryWrites=true&w=majority")
    db = client['billing']
    bills_collection = db['bills']
    print("✅ Connected to MongoDB!")
except Exception as e:
    print("❌ Connection failed:", e)

@app.route('/')
def index():
    success = request.args.get('success')
    customer = request.args.get('customer')
    amount = request.args.get('amount')
    return render_template('index.html', success=success, customer=customer, amount=amount)

@app.route('/add_bill', methods=['POST'])
def add_bill():
    customer = request.form.get('customer')
    phone = request.form.get('phone')

    items = []
    index = 0
    total_amount = 0

    while True:
        name = request.form.get(f'items[{index}][name]')
        qty = request.form.get(f'items[{index}][quantity]')
        price = request.form.get(f'items[{index}][price]')

        # Stop the loop if item name is missing
        if not name:
            break

        # Skip this item if quantity or price is missing
        if  not price:
            index += 1
            continue

        try:
            qty = int(qty) if qty else 1
            price = float(price)
        except ValueError:
            index += 1
            continue  # skip invalid row

        item_total = qty * price

        items.append({
            'name': name,
            'quantity': qty,
            'price': price,
            'total': round(item_total, 2)
        })

        total_amount += item_total
        index += 1

    data = {
        "customer": customer,
        "phone": phone if phone else None,
        "items": items,
        "amount": round(total_amount, 2),
        "date": datetime.datetime.now()
    }

    bills_collection.insert_one(data)

    return redirect(url_for('index', success=1, customer=customer, amount=round(total_amount, 2)))

@app.route('/bills')
def view_bills():
    bills = list(bills_collection.find())
    return render_template('bills.html', bills=bills)

if __name__ == '__main__':
    app.run(debug=True)
