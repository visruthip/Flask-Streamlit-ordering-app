from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    drink = db.Column(db.String(80), nullable=False)
    size = db.Column(db.String(80), nullable=False)

@app.route('/order', methods=['POST'])
def order():
    data = request.json
    name = data['name']
    drink = data['drink']
    size = data['size']

    existing_order = Order.query.filter_by(name=name).first()
    if existing_order:
        return jsonify({'error': 'Order with this name already exists.'}), 400

    new_order = Order(name=name, drink=drink, size=size)
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({'message': 'Order placed successfully'}), 200

@app.route('/orders', methods=['GET'])
def orders():
    all_orders = Order.query.all()
    orders_list = [{'name': order.name, 'drink': order.drink, 'size': order.size} for order in all_orders]
    return jsonify(orders_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the tables within the app context
    app.run(debug=True)
