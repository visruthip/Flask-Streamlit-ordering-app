[Link to view the application](http://3.112.123.128:8501/)

### Project Structure

```
order_management/
│
├── app.py                # Streamlit frontend
├── backend.py            # Flask backend
├── requirements.txt      # Dependencies
├── templates/            # HTML templates for Flask (optional)
│   ├── index.html
│   └── orders.html
└── orders.db             # SQLite database (will be created automatically)
```

### Step 1: Flask Backend (`backend.py`)

This file will hold your existing Flask code, slightly modified to allow for API interactions with the Streamlit frontend.

```python
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

```

### Step 2: Streamlit Frontend (`app.py`)

This file will interact with your Flask backend to place orders.

```python
import streamlit as st
import requests
import pandas as pd

# Title of the application
st.title("Order Management System")

# Input fields for placing an order
st.header("Place your Order here")

name = st.text_input("Name:")
drink = st.text_input("Order:")
size = st.selectbox("Size:", ["Small", "Medium", "Large"])

# Submit button to place the order
if st.button("Submit"):
    if name and drink and size:
        # Sending order to Flask backend
        response = requests.post("http://127.0.0.1:5000/order", json={
            "name": name,
            "drink": drink,
            "size": size
        })
        
        if response.status_code == 200:
            st.success(f"Order placed successfully!\n\nName: {name}\nOrder: {drink}\nSize: {size}")
        else:
            st.error(response.json().get('error', 'An error occurred.'))
    else:
        st.error("Please fill in all fields.")

# Button to display all orders
if st.button("Show All Orders"):
    response = requests.get("http://127.0.0.1:5000/orders")
    if response.status_code == 200:
        orders = response.json()
        if orders:
            # Convert orders to DataFrame for tabular display
            df_orders = pd.DataFrame(orders)
            st.subheader("Current Orders:")
            st.markdown("**Name | Order | Size**")  # Bold header
            st.table(df_orders)  # Display in a table format
        else:
            st.write("No orders found.")
    else:
        st.error("Failed to retrieve orders.")

```


### Step 3: Requirements File (`requirements.txt`)

Create a `requirements.txt` to manage your dependencies:

```
Flask==2.0.3
Flask-SQLAlchemy==2.5.1
streamlit==1.9.0
requests==2.26.0
pandas==1.3.5
```

### Templates is Optional, as we are using streamline for this project

### Step 4: Running the Application
```bash
mkdir VisruthiFlaskStreamlitAPI
cd VisruthiFlaskStreamlitAPI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backend.py
streamlit run app.py #in another terminal

   ```

### Notes

- Make sure to run the Flask server before starting the Streamlit app, as the Streamlit app will send requests to the Flask server.

### Testing:
[Link to view the application](http://3.112.123.128:8501/)

Place your orders below, once you open the weblink:

<img width="409" alt="image" src="https://github.com/user-attachments/assets/f6bd60fd-d537-4df9-aa41-f383feacf2c5">

Click on "Show All Orders" to view order history:

<img width="376" alt="image" src="https://github.com/user-attachments/assets/8b308c11-1fc4-4082-bff3-8d298db43781">


### Thank you :)




