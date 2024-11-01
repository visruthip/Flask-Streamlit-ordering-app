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
