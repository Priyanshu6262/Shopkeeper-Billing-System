import tkinter as tk
from tkinter import messagebox, font
import mysql.connector
from tkcalendar import DateEntry
from datetime import datetime

# Connect database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Priyanshu@123",
    database="shopkeeper"
)
cursor = conn.cursor()

# Global variable to store bill items
bill_items = []
payment_type = None

# Function to add item to the bill
def add_item():
    try:
        name = entry_name.get()
        phone_number = entry_phone.get()
        date = entry_date.get()
        goods = entry_goods.get()
        quantity = int(entry_quantity.get())
        price = float(entry_price.get())
        total = quantity * price

        # Store item data in the bill_items list
        bill_items.append((goods, quantity, price, total))
        display_text = f"{goods} - Qty: {quantity}, Price: {price}, Total: {total}\n"
        text_display.insert(tk.END, display_text)

        cursor.execute("INSERT INTO bill_items (name, phone_number, date, goods, quantity, price, total_amount) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (name, phone_number, date, goods, quantity, price, total))
        conn.commit()

        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"Error adding item: {e}")

# Function to clear input fields
def clear_fields():
    entry_goods.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)

# Function to finalize and display the bill
def finalize_bill():
    # Get customer information
    name = entry_name.get()
    phone_number = entry_phone.get()
    date = entry_date.get()

    # Clear the display area
    text_display.delete("1.0", tk.END)

    # Display name and phone number in bold at the top
    text_display.insert(tk.END, f"Name: {name}\nPhone: {phone_number}\n", ("bold"))

    # Calculate and display items with total
    total_price = 0
    for item in bill_items:
        goods, quantity, price, item_total = item
        text_display.insert(tk.END, f"{goods} - Qty: {quantity}, Price: {price}, Total: {item_total}\n")
        total_price += item_total

    # Show the total price at the bottom
    text_display.insert(tk.END, f"\nTotal Price: {total_price}\n", ("bold",))
    
    # Store the complete bill in the database
    try:
        cursor.execute("INSERT INTO bills (name, phone_number, date, total_amount) VALUES (%s, %s, %s, %s)",
                   (name, phone_number, entry_date.get(), total_price))
        conn.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error inserting data: {err}")


    # Clear input fields and bill_items
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_goods.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    bill_items.clear()

# Function to remove all items
def remove_bill():
    text_display.delete("1.0", tk.END)
    bill_items.clear()

root = tk.Tk()
root.title("BillBharat")
root.geometry("650x450") 
root.configure(bg="#D3D3D3")


# Custom font for bold text
bold_font = font.Font(root, weight="bold")
text_display = tk.Text(root, width=40, height=25)
text_display.tag_configure("bold", font=bold_font)

# Frames for layout
display_frame = tk.Frame(root)
display_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

input_frame = tk.Frame(root)
input_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

# Big display area
text_display = tk.Text(display_frame, width=40, height=25)
text_display.pack()

# Input fields
tk.Label(input_frame, text="Name").grid(row=0, column=0, sticky="w")
entry_name = tk.Entry(input_frame, width=25,bg='#FFFFE0')
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Phone Number").grid(row=1, column=0, sticky="w")
entry_phone = tk.Entry(input_frame, width=25,bg='#FFFFE0')
entry_phone.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Date").grid(row=2, column=0, sticky="w")
entry_date = DateEntry(input_frame, width=22, date_pattern="yyyy-mm-dd",bg='#FFFFE0')
entry_date.grid(row=2, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Goods").grid(row=3, column=0, sticky="w")
entry_goods = tk.Entry(input_frame, width=25,bg='#FFFFE0')
entry_goods.grid(row=3, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Quantity").grid(row=4, column=0, sticky="w")
entry_quantity = tk.Entry(input_frame, width=25,bg='#FFFFE0')
entry_quantity.grid(row=4, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Price").grid(row=5, column=0, sticky="w")
entry_price = tk.Entry(input_frame, width=25,bg='#FFFFE0')
entry_price.grid(row=5, column=1, padx=5, pady=5)

# Payment Type
tk.Label(input_frame, text="Payment Type").grid(row=6, column=0, sticky="w")
payment_var = tk.StringVar()
payment_options = tk.OptionMenu(input_frame, payment_var, "Cash", "Online")
payment_options.grid(row=6, column=1, padx=5, pady=5)

# Buttons
btn_add = tk.Button(input_frame, text="Add", width=10, command=add_item,bg='#4CAF50')
btn_add.grid(row=7, column=0, pady=10)

btn_bill = tk.Button(input_frame, text="Bill", width=10, command=finalize_bill,bg='#4CAF50')
btn_bill.grid(row=7, column=1, pady=10)

btn_remove_bill = tk.Button(input_frame, text="Remove Bill", width=20, command=remove_bill,bg='#FF4500')
btn_remove_bill.grid(row=8, column=0, columnspan=2, pady=5)

root.mainloop()

# Close the database connection
cursor.close()
conn.close()
