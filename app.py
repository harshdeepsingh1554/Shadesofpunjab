from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import datetime
import os

app = Flask(__name__)

# ✅ Use environment variable for MongoDB URI
MONGO_URI = os.environ.get("MONGO_URI")

try:
    client = MongoClient(MONGO_URI)
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

        if not name:
            break

        try:
            qty = int(qty) if qty else 1
            price = float(price)
        except ValueError:
            index += 1
            continue

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
