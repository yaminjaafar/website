# flask app
from flask import *
import json
import sqlite3

# generate 5 random number for order code
import random

app = Flask(__name__)
database_name = 'database.db'


# sqlite database

def create_connection():
    try:
        conn = sqlite3.connect(database_name)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None


diy_acai_items = {
    "diy_acai_items_size_options": [
        {'name': 'small', 'price': '7.40'},
        {'name': 'medium', 'price': '10.80'},
        {'name': 'large', 'price': '16.40'}
    ],
    "fruit_options": [
        {
            "name": "Banana",
            "sizes": [{"name": "small", "price": 2}, {"name": "medium", "price": 3}, {"name": "large", "price": 5}]
        },
        {
            "name": "Strawberry",
            "sizes": [{"name": "small", "price": 2}, {"name": "medium", "price": 3}, {"name": "large", "price": 5}]
        },
        {
            "name": "Blueberry",
            "sizes": [{"name": "small", "price": 2}, {"name": "medium", "price": 3}, {"name": "large", "price": 5}]
        },
        {
            "name": "Kiwi",
            "sizes": [{"name": "small", "price": 2}, {"name": "medium", "price": 3}, {"name": "large", "price": 5}]
        },
        {
            "name": "Dragonfruit",
            "sizes": [{"name": "small", "price": 2}, {"name": "medium", "price": 3}, {"name": "large", "price": 5}]
        },
        {
            "name": "Pineapple",
            "sizes": [{"name": "small", "price": 2}, {"name": "medium", "price": 3}, {"name": "large", "price": 5}]
        }
    ],
    "superfood_options": [
        {
            "name": 'granola',
            "sizes": [{"size": 'small', "price": 2}, {"size": 'medium', "price": 3}, {"size": 'large', "price": 4}]
        },
        {
            "name": 'almond flakes',
            "sizes": [{"size": 'small', "price": 2}, {"size": 'medium', "price": 3}, {"size": 'large', "price": 4}]
        },
        {
            "name": 'pumpkin seeds',
            "sizes": [{"size": 'small', "price": 2}, {"size": 'medium', "price": 3}, {"size": 'large', "price": 4}]
        },
        {
            "name": 'cacao nibs',
            "sizes": [{"size": 'small', "price": 2}, {"size": 'medium', "price": 3}, {"size": 'large', "price": 4}]
        },
        {
            "name": 'chia seeds',
            "sizes": [{"size": 'small', "price": 2}, {"size": 'medium', "price": 3}, {"size": 'large', "price": 4}]
        },
        {
            "name": 'coconut shavings',
            "sizes": [{"size": 'small', "price": 2}, {"size": 'medium', "price": 3}, {"size": 'large', "price": 4}]
        },
        {
            "name": 'goji berries',
            "sizes": [{"size": 'small', "price": 2}, {"size": 'medium', "price": 3}, {"size": 'large', "price": 4}]
        }
    ],
    "dizzle_options": [
        {"name": 'honey', "price": 0},
        {"name": 'cookie butter', "price": 0},
        {"name": 'almond butter', "price": 0},
        {"name": 'peanut butter', "price": 0},
        {"name": 'cashew butter', "price": 1}]
}

toast_items = []
acai_items = []
smoothies_and_drinks_items = []
# diy_acai
diy_acai_items_size_options = []
base_a_options = []
base_b_options = []
fruit_options = []
superfood_options = []
dizzle_options = []

db = create_connection()

if db is not None:
    cursor = db.cursor()
    # get data
    query = "SELECT * FROM toast_items"
    cursor.execute(query)
    toast_items_ = cursor.fetchall()
    for item in toast_items_:
        toast_items.append({
            "id": item[0],
            "name": item[1],
            "price": item[2],
            "description": item[3]
        })

    query = "SELECT * FROM acai_items"
    cursor.execute(query)
    acai_items_ = cursor.fetchall()

    for item in acai_items_:
        acai_items.append({
            "name": item[1],
            "description": item[2],
            "image": item[3],
            "sizes": json.loads(item[4])
        })
    query = "SELECT * FROM smoothies_and_drinks_items"
    cursor.execute(query)
    smoothies_and_drinks_items_ = cursor.fetchall()

    for item in smoothies_and_drinks_items_:
        smoothies_and_drinks_items.append({
            "name": item[1],
            "description": item[2],
            "sizes": json.loads(item[3])
        })

    # get diy_acai_items_size_options
    query = "SELECT * FROM diy_acai_items_size_options"
    cursor.execute(query)
    diy_acai_items_size_options_ = cursor.fetchall()
    for item in diy_acai_items_size_options_:
        diy_acai_items_size_options.append({
            "name": item[1],
            "price": item[2]
        })

    # get diy_acai_items
    query = "SELECT * FROM diy_acai_items_base_a_options"
    cursor.execute(query)
    base_a_options_ = cursor.fetchall()
    for item in base_a_options_:
        base_a_options.append({
            "name": item[1],
            "price": item[2]
        })

    query = "SELECT * FROM diy_acai_items_base_b_options"
    cursor.execute(query)
    base_b_options_ = cursor.fetchall()
    for item in base_b_options_:
        base_b_options.append({
            "name": item[1],
            "price": item[2]
        })

    db.commit()
    db.close()


def add_order(user_id, items, total, status, order_type):
    db = create_connection()
    if db is not None:
        cursor = db.cursor()
        query = "INSERT INTO orders (user_id, items, total, status, order_type) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (user_id, json.dumps(items), total, status, order_type))
        db.commit()
        db.close()


def get_pending_orders(user_id):
    db = create_connection()
    pending_orders = []

    if db is not None:
        cursor = db.cursor()
        query = "SELECT * from orders where user_id = ? AND status = 'pending'"
        cursor.execute(query, (user_id,))
        orders = cursor.fetchall()
        for order in orders:
            print(order)
            d = json.loads(order[2])

            pending_orders.append((order[0], order[1], d, order[3], order[4], order[5], order[6]))

        db.close()
    return pending_orders


pending_orders_codes = []


def get_received_orders():
    global pending_orders_codes
    pending_orders_codes = []
    orders = []
    db = create_connection()
    if db is not None:
        cursor = db.cursor()
        query = "SELECT o.id, u.username,o.items, o.total, o.status, o.date  from orders o join users u ON o.user_id = u.id  where status = 'pending'"
        cursor.execute(query)
        for order in cursor.fetchall():

            code = ''
            for i in range(5):
                code += str(random.randint(0, 9))
            pending_orders_codes.append((code, order[0]))
            orders.append([order[0], order[1], json.loads(order[2]), order[3], order[4], order[5], code])
        db.close()
        return orders


def count_pending_orders():
    db = create_connection()
    if db is not None:
        cursor = db.cursor()
        query = "SELECT COUNT(*) from orders where status = 'pending'"
        cursor.execute(query)
        count = cursor.fetchone()
        db.close()
        return count[0]


def get_user_data(user_id):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    db.close()
    return user


# Dummy user dat
# set template folder
app.template_folder = 'templates'

# set static folder
app.static_folder = 'static'


@app.route('/')
def home():
    # get redirect data - user_id, user_name, user_email, user_account_type
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    user_email = request.args.get('user_email')
    user_account_type = request.args.get('user_account_type')

    return render_template('index.html', toast_items=toast_items, acai_items=acai_items,
                           smoothies_and_drinks_items=smoothies_and_drinks_items,
                           items_size_options=json.dumps(diy_acai_items_size_options),
                           base_a_options=json.dumps(base_a_options),
                           base_b_options=json.dumps(base_b_options),
                           fruit_options=json.dumps(diy_acai_items['fruit_options']),
                           superfood_options=json.dumps(diy_acai_items['superfood_options']),
                           dizzle_options=json.dumps(diy_acai_items['dizzle_options']),
                           pending_orders_count=count_pending_orders(),
                           login=True, user_id=user_id,
                           user_name=user_name,
                           user_email=user_email,
                           user_account_type=user_account_type)

# signup or logup or
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # account_type = request.form['account_type']
        address = request.form['address']


        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        query = "INSERT INTO users (name, email, password, account_type, address) VALUES (?, ?, ?, 0, ?)"
        cursor.execute(query, (name, email, password, address))
        db.commit()
        db.close()
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        db.close()
        if user is not None:
            id_, username, email, password, account_type, address = user
            
            # redirect to home page with user data
            return render_template('login_success.html', user_id=id_, username=username, email=email,
                                   account_type=account_type, address=address)
    return render_template('login.html')


@app.route('/login_success')
def login_success():
    return render_template('login_success.html')


@app.route('/menu')
def menu():
    # toast_items
    # acai_items
    # smoothies_and_drinks_items
    return render_template('menu.html', toast_items=toast_items, acai_items=acai_items,
                           smoothies_and_drinks_items=smoothies_and_drinks_items)


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/orders-received')
def orders():
    user_id = request.args.get('user_id')
    orders_received = get_received_orders()
    return render_template('orders.html', orders_received=orders_received)


@app.route('/order', methods=['POST'])
def post():
    try:
        data = request.json
        user_id = data['user_id']
        order_data = data['order_data']
        total = data['total_price']
        status = data['status']
        order_type = data['order_type']
        print('data: ', data)
        add_order(user_id, order_data, total, status, order_type)
    except Exception as e:
        print(e)
        return jsonify({'success': False})
    return jsonify({'success': True})


@app.route('/pending-orders', methods=['GET'])
def online_pending_orders():
    user_id = request.args.get('user_id')  # get user_id from query params like
    print(user_id)
    pending_orders = get_pending_orders(user_id)
    return render_template('pending_orders.html', pending_orders=pending_orders)


@app.route('/receive_order', methods=['POST'])
def receive_order():
    # get json data
    data = request.json
    order_id = data['order_id']
    receiving_code = data['receiving_code']
    user_id = data['user_id']

    for code, id_ in pending_orders_codes:
        if code == receiving_code and id_ == int(order_id):
            db = create_connection()
            if db is not None:
                cursor = db.cursor()

                # check if order is pending
                query = "SELECT * FROM orders WHERE id = ? and status = 'pending' and user_id = ?"
                cursor.execute(query, (order_id, user_id))
                order = cursor.fetchall()
                if len(order) == 0:
                    return jsonify({'success': False})

                query = "UPDATE orders SET status = 'received' WHERE id = ? and status = 'pending' and user_id = ?"
                cursor.execute(query, (order_id, user_id))

                db.commit()
                db.close()
                return jsonify({'success': True})

    return jsonify({'success': False})


# delete order received /order/id/delete
@app.route('/order/<int:id>/delete', methods=['GET'])
def delete_order(id):
    db = create_connection()
    if db is not None:
        cursor = db.cursor()
        query = "DELETE FROM orders WHERE id = ?"
        cursor.execute(query, (id,))
        db.commit()
        db.close()
    return redirect(url_for('orders'))


@app.route('/logout', methods=['GET'])
def logout():
    return render_template('logout.html')


if __name__ == '__main__':
    app.run(debug=True)
