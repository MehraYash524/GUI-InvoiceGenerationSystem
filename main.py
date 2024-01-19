# Importing Necessary Dependencies
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import random
import os
from PIL import Image, ImageTk
import tempfile

# Connect to the MySQL database
db = mysql.connector.connect(host="your host name",
                             user="user name",
                             password="password",
                             database="database name")

#Define global variables for entry widget, global_saved_bill_textarea, name_textarea avoiding future errors
bill_number_entry = None
global_saved_bill_textarea = None
name_textarea = None

# This function edit the text
def edit_text(text_widget, start, end, font, size):
    
    text_widget.tag_configure("bold", font=(font, size, "bold"))
    start_index = text_widget.search(start, "1.0", tk.END)
    end_index = text_widget.search(end, "1.0", tk.END)
    text_widget.tag_add("bold", start_index, end_index + f"+{len(end)}c")


# Generate a random bill number
def generate_unique_bill_number(): 
    return random.randint(1000, 9999)


# Function to insert a new bill with a random bill number
def insert_bill(customer_name, phone_number, email, product_category, sub_category, quantity, price, bill_number):
    # Validate input fields
    if not customer_name or not phone_number or not email:
        show_error("Please fill in all customer details.")
        return

    if not product_category or not sub_category or not quantity:
        show_error("Please fill in all product details.")
        return

    try:
        quantity = int(quantity)
        if quantity <= 0:
            show_error("Quantity should be a positive integer.")
            return
    except ValueError:
        show_error("Quantity should be a positive integer.")
        return

    try:
        cursor = db.cursor()
        total_price = float(price) * quantity
        cursor.execute("INSERT INTO bills (bill_number, customer_name, phone_number, email, product_category, sub_category, quantity, price, total_price) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s)",
                       (bill_number, customer_name, phone_number, email, product_category, sub_category, quantity, price, total_price))
        db.commit()
        cursor.close()

        
    except Exception as e:
        show_error(f"An error occurred: {str(e)}")

    
# Function to display an error message
def show_error(message):
    messagebox.showerror("Error", message)
    
    
# Function to search for a bill
def search_bill():
    global bill_number_entry
    global name_textarea
    search_window = tk.Toplevel(root)
    search_window.title("Search Bill")
    
    # To see the window in Fullscreen
    search_window.attributes("-fullscreen", True)
    
    #Uploading Image
    img=Image.open("images/Services.jpg")
    photoimg=ImageTk.PhotoImage(img)

    img_lbl = tk.Label(search_window, image=photoimg)
    img_lbl.place(x=0,y=0, width=1366, height=768)
    
    img_lbl.image = photoimg

    # logic GUI
    bill_number_label = tk.Label(search_window, text="Enter Bill Number:", font=("open sans", 15, "bold"), fg="#06392e", bd=0, highlightthickness=0, bg="white")
    bill_number_entry = tk.Entry(search_window, font=("open sans", 15))

    search_button = tk.Button(search_window, text="Search", font=("open sans", 15, "bold"), fg="#06392e", bd=0, highlightthickness=0, bg="white", command=lambda: display_searched_bill(bill_number_entry.get()), cursor="hand2")

    bill_number_label.place(relx=0.65, rely=0.3, width=200, height=50, anchor="center")
    bill_number_entry.place(relx=0.82, rely=0.3, width=200, height=50, anchor="center")
    search_button.place(relx=0.735, rely=0.4, width=420, height=50, anchor="center")
    
    #clear button
    clear_button = tk.Button(search_window, text="Back", font=("open sans", 15, "bold"), fg="#06392e", command=lambda:exit(search_window), bd=0, highlightthickness=0, bg="white", cursor="hand2")
    clear_button.place(relx=0.24, rely=0.62, width=200, height=50, anchor="center")
    
    #bill number names and date
    right = tk.LabelFrame(search_window, text=f"", fg="#06392e", bg="white")
    right.place(x=730, y=352, width=420, height=250)
    
    scroll_y = tk.Scrollbar(right, orient="vertical")
    
    textarea = tk.Text(right, yscrollcommand=scroll_y.set, bg="white", fg="black")
    
    name_textarea = textarea
    
    def show_all_names():
        global name_textarea
        # Retrieve bill number
        cursor = db.cursor()
        cursor.execute("SELECT bill_number, customer_name, min(timestamp) FROM bills group by 1,2")
        bill_info = cursor.fetchall()

        cursor.close()
        
        name_textarea.config(state="normal")
        name_textarea.delete(1.0, tk.END)
        
        name_textarea.insert(tk.END, "---------------------------------------------------\n"
                                                        "                       Bills \n"
                                                        "---------------------------------------------------") 
        name_textarea.insert(tk.END, f" Search bill by name:\n\n")
        
        name_textarea.insert(tk.END, "\n Name\t\t Bill No.\t\tDate\n")  
        
        for i in bill_info:
            info = f"\n {i[1]:<15}\t\t{i[0]:<5}\t\t {i[2].strftime('%B %d, %Y')}"
            name_textarea.insert(tk.END, info)
            
        edit_text(name_textarea, "Bills", "Bills", "times new roman", 15)
        
        name_textarea.config(state="disabled")
        name_textarea.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
    
    def search_name(name):
        global name_textarea
         # Retrieve bill number
        cursor = db.cursor()
        cursor.execute("SELECT bill_number, customer_name, min(timestamp) FROM bills where customer_name = %s group by 1,2", (name,))
        bill_info = cursor.fetchall()
        cursor.close()
        
        
        name_textarea.config(state="normal")
        name_textarea.delete(1.0, tk.END)
        
        
        name_textarea.insert(tk.END, "---------------------------------------------------\n"
                                                      "                       Bills \n"
                                                      "---------------------------------------------------") 
        name_textarea.insert(tk.END, f" Search bill by name:\n\n")
        
        name_textarea.insert(tk.END, "\n Name\t\t Bill No.\t\tDate\n")  
        
        for i in bill_info:
            info = f"\n {i[1]:<15}\t\t{i[0]:<5}\t\t {i[2].strftime('%B %d, %Y')}"
            name_textarea.insert(tk.END, info)
            
        edit_text(name_textarea, "Bills", "Bills", "times new roman", 15)
        
        name_textarea.config(state="disabled")
        name_textarea.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
    
        
        
        
    show_all_names() # Initially show all names in search window
    
    name_entry = tk.Entry(search_window, font=("open sans", 9), bg="white", fg="black", bd=2)
    name_entry.place(relx=0.615, rely=0.615, width=100, height=20, anchor="center")
    
    name_search_button = tk.Button(search_window, text="Search", font=("open sans", 9), fg="black", command=lambda:search_name(name_entry.get()), bd=2, highlightthickness=0, bg="white", cursor="hand2")
    name_search_button.place(relx=0.68, rely=0.615, width=45, height=20, anchor="center")
    
    clear_name_button = tk.Button(search_window, text="Clear", font=("open sans", 9), fg="black", command=lambda:show_all_names(), bd=2, highlightthickness=0, bg="white", cursor="hand2")
    clear_name_button.place(relx=0.72, rely=0.615, width=45, height=20, anchor="center")

# Function for destroying any window
def exit(root):
    #Close the window
    root.destroy()

def save_bill(bill_number, searched_bill_window):
    global global_saved_bill_textarea
    op = messagebox.askyesno("Save Bill", "Do you want to save the Bill?", parent = searched_bill_window)
    if op > 0:
        bill_data = global_saved_bill_textarea.get(1.0, tk.END)
        with open('bills/' + str(bill_number) + ".txt", 'w') as f:
            f.write(bill_data)
        op = messagebox.showinfo("Saved", f"Bill No: {bill_number} saved successfully:)")
        
def print_bill():
    q= global_saved_bill_textarea.get(1.0, "end-1c")
    filename = tempfile.mktemp('.txt')
    open(filename, 'w').write(q)
    os.startfile(filename, "Print")
        


# Function to display the details of the searched bill
def display_searched_bill(bill_number):
    global global_saved_bill_textarea
    global global_total_price
    if not bill_number:
        show_error("Please enter a bill number.")
        return    

    searched_bill_window = tk.Toplevel(root)
    searched_bill_window.title("Searched Bill")
    
    
    main_frame = tk.Frame(searched_bill_window,bd=0, relief="flat",bg="white" )
    main_frame.place(x=0,y=0,width=1530, height=800)
    
     # To see the window in Fullscreen
    searched_bill_window.attributes("-fullscreen", True)
    
    #Uploading Image
    img=Image.open("images/Services.jpg")
    photoimg=ImageTk.PhotoImage(img)

    img_lbl = tk.Label(main_frame, image=photoimg)
    img_lbl.place(x=0,y=0, width=1366, height=768)
    
    img_lbl.image = photoimg

    # Retrieve bill details from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM bills WHERE bill_number = %s", (bill_number,))
    bill_details = cursor.fetchall()
    cursor.close()
    db.commit()

    if not bill_details:
        messagebox.showinfo("Result", f"No bill found with Bill Number: {bill_number}")
        return
    right = tk.LabelFrame(main_frame, text=f"#{bill_number}", font=("open sans", 15, "bold"), fg="#06392e", bg="white")
    right.place(x=715, y=152, width=480, height=440)
    
    scroll_y = tk.Scrollbar(right, orient="vertical")
    
    textarea = tk.Text(right, yscrollcommand=scroll_y.set, bg="white", fg="black")

    
    textarea.insert(tk.END, "----------------------------------------------------------\n"
                                                      "                         INVOICE \n"
                                                      "----------------------------------------------------------")
    textarea.insert(tk.END, f"\n Bill Number: {bill_details[0][0]}\n"
                                                              f" Date: {bill_details[0][9].strftime('%B %d, %Y')}\n\n"
                                                              " Customer Information:\n"
                                                              f" Name: {bill_details[0][1]}\n"
                                                              f" Phone: {bill_details[0][2]}\n"
                                                              f" Email: {bill_details[0][3]}\n\n"
                                                              )
    
    
    total_price = 0
    
    #insert header
    textarea.insert(tk.END, "----------------------------------------------------------")
    textarea.insert(tk.END, "\n Products\t\t\tPrice\tQty.\tTotal")
    textarea.insert(tk.END, "\n----------------------------------------------------------")

    for row in bill_details:
        product_info = f"\n {row[5]:<15}\t\t\t${row[7]:<5}\t{row[6]:<3}\t${row[8]:<5}"
        textarea.insert(tk.END, product_info)

        total_price += row[8]
        

    # Insert footer
    textarea.insert(tk.END, "\n----------------------------------------------------------")
    textarea.insert(tk.END, f"\n {'Total:':<26}\t\t\t\t\t${total_price:<5}")
    textarea.insert(tk.END, "\n Thank you for your purchase!\nVisit again soon.\n")
    "\nThank you for your purchase! \n Visit again soon.\n" + "-" * 39
    textarea.insert(tk.END, "\n----------------------------------------------------------")
    
    edit_text(textarea, "INVOICE", "INVOICE", "times new roman", 15)
    
    
    textarea.config(state="disabled")
    textarea.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    global_saved_bill_textarea = textarea

    close_button = tk.Button(right, text="X", font=("open sans", 12, "bold"), fg="white", command=lambda:exit(root), bd=0, highlightthickness=0, bg="red3", cursor="hand2")
    close_button.place(relx=0.97, rely=-0.04, width=30,height=20,anchor="center")
    
    save_button = tk.Button(searched_bill_window, text="Save", font=("open sans", 15, "bold"), fg="#06392e", command=lambda:save_bill(bill_number,searched_bill_window),bd=0, highlightthickness=0, bg="white", cursor="hand2")
    save_button.place(relx=0.24, rely=0.62, width=200, height=50, anchor="center")
    
    print_button = tk.Button(searched_bill_window, text="Print", font=("open sans", 15, "bold"), fg="#06392e", command=lambda : print_bill(), bd=0, highlightthickness=0, bg="white", cursor="hand2")
    print_button.place(relx=0.419, rely=0.62, width=200,height=50,anchor="center")

    

# Function to show the product category form
def show_product_category(customer_name, phone_number, email,bill_number, prev_window):

    # Validate input fields
    if not customer_name or not phone_number or not email:
        show_error("Please fill in all customer details.")
        return

    # Destroy the previous window
    prev_window.destroy()

    product_category_window = tk.Toplevel(root)
    product_category_window.title("Product Category")
    
    # To see the window in Fullscreen
    product_category_window.attributes("-fullscreen", True)
    
    #Uploading Image
    img=Image.open("images/Services.jpg")
    photoimg=ImageTk.PhotoImage(img)

    img_lbl = tk.Label(product_category_window, image=photoimg)
    img_lbl.place(x=0,y=0, width=1366, height=768)
    
    img_lbl.image = photoimg


    # Getting the price of current selected product    
    def selct(event):
        selectd_price = sub_category_entry.get()
        
        # Retrieve price from the database based on the selected category
        cursor = db.cursor()
        cursor.execute(f"SELECT price FROM products WHERE product_name = %s ", (selectd_price,))
        product_info = cursor.fetchall()
        
        cursor.close()
        # Extract product names and prices from the query result
        product_price = [info[0] for info in product_info]
        
        # Update sub_category_entry and price_entry with the retrieved data
        price_entry.config(value=product_price)
        price_entry.current(0)
    
    
    # Retriving categories from the database to show in the combobox of product category
    def category():
         # Retrieve product category from the database
        cursor = db.cursor()
        cursor.execute(f"SELECT distinct category FROM products")
        product_info = cursor.fetchall()
        cursor.close()
        # Extract product_category from the query result
        product_category = [info for info in product_info]
        return product_category
        
 
    def sub_total(event):
        try:
            price = float(price_entry.get())  # Assuming price is a float
            quantity = int(quantity_entry.get())
            total_price = price * quantity
            total_entry.config(state="normal")  # Allow modifications to the entry
            total_entry.delete(0, tk.END)  # Clear previous value
            total_entry.insert(0, f"{total_price:.2f}")  # Set the new total price
            
            total_entry.config(state="readonly")  # Make the entry read-only again
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for Price and Quantity.")

    
    product_category_label = tk.Label(product_category_window, text="Product Category:", font=("open sans", 15, "bold"), fg="#06392e", bd=0, highlightthickness=0, bg="white")
    product_category_combobox = ttk.Combobox(product_category_window, values=category(), font=("open sans", 15, "bold"))  # Add actual categories here by pssing values = category()


    sub_category_label = tk.Label(product_category_window, text="Product Name:", font=("open sans", 15, "bold"), fg="#06392e", bd=0, highlightthickness=0, bg="white")
    sub_category_entry = ttk.Combobox(product_category_window, font=("open sans", 15))

    quantity_label = tk.Label(product_category_window, text="Quantity:", font=("open sans", 15, "bold"), fg="#06392e", bd=0, highlightthickness=0, bg="white")
    quantity_entry = tk.Entry(product_category_window, font=("open sans", 15))
    
    price_label = tk.Label(product_category_window, text="price:", font=("open sans", 15, "bold"), fg="#06392e", bd=0, highlightthickness=0, bg="white")
    price_entry = ttk.Combobox(product_category_window, font=("open sans", 15), state="readonly")
    
    
    total_label = tk.Label(product_category_window, text="Sub Total:", font=("open sans", 15, "bold"), fg="#06392e", bd=0, highlightthickness=0, bg="white")
    total_entry = tk.Entry(product_category_window, font=("open sans", 15), state="readonly")
    
    next_button = tk.Button(product_category_window, text="Next", font=("open sans", 12, "bold"), fg="white", bd=0, highlightthickness=0, bg="green", command=lambda: display_searched_bill(bill_number), cursor="hand2")
    
    addcart_button = tk.Button(product_category_window, text="Add to Cart", font=("open sans", 15, "bold"), fg="#06392e", command=lambda: insert_bill(customer_name, phone_number, email, product_category_combobox.get(), sub_category_entry.get(), int(quantity_entry.get()), float(price_entry.get()), bill_number), bd=0, highlightthickness=0, bg="white")
    
    
    product_category_label.place(relx=0.65, rely=0.3, width=200, height=50, anchor="center")
    product_category_combobox.place(relx=0.82, rely=0.3, width=200, height=50, anchor="center")

    sub_category_label.place(relx=0.65, rely=0.4, width=200, height=50, anchor="center")
    sub_category_entry.place(relx=0.82, rely=0.4, width=200, height=50, anchor="center")

    quantity_label.place(relx=0.65, rely=0.5, width=200, height=50, anchor="center")
    quantity_entry.place(relx=0.82, rely=0.5, width=200, height=50, anchor="center")
    
    price_label.place(relx=0.65, rely=0.6, width=200, height=50, anchor="center")
    price_entry.place(relx=0.82, rely=0.6, width=200, height=50, anchor="center")

    total_label.place(relx=0.65, rely=0.7, width=200, height=50, anchor="center")
    total_entry.place(relx=0.82, rely=0.7, width=200, height=50, anchor="center")

    
    next_button.place(relx=0.875, rely=0.77, width=60,height=30,anchor="center")
    
    addcart_button.place(relx=0.65, rely=0.8, width=200, height=50, anchor="center")

    # Bind the update_subcategory function to the <<ComboboxSelected>> event
    product_category_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=product_category_combobox: update_subcategory(event,combobox,sub_category_entry))
    
    sub_category_entry.bind("<<ComboboxSelected>>", selct)
    
    # Bind the <Return> key to the sub_total function
    quantity_entry.bind("<Return>", sub_total)


    #clear button
    clear_button = tk.Button(product_category_window, text="Back", font=("open sans", 15, "bold"), fg="#06392e", command=lambda:exit(product_category_window), bd=0, highlightthickness=0, bg="white")
    clear_button.place(relx=0.24, rely=0.62, width=200, height=50, anchor="center")


def update_subcategory(event, product_category_combobox,sub_category_entry):
    selected_category = product_category_combobox.get()
    
    # Retrieve product name from the database based on the selected category
    cursor = db.cursor()
    cursor.execute(f"SELECT product_name, price FROM products WHERE category = %s ", (selected_category,))
    product_info = cursor.fetchall()
    cursor.close()
    
    # Extract product names and prices from the query result
    product_names = [info[0] for info in product_info]

    # Update sub_category_entry and price_entry with the retrieved data
    sub_category_entry.config(value=product_names)
    sub_category_entry.current(0)
    
    

# Function to show the customer details form
def show_customer_details():
    
    # Generate a unique bill number
    bill_number = generate_unique_bill_number()

    customer_details_window = tk.Toplevel(root)
    customer_details_window.title("Customer Details")
    
    # Set the new window to full-screen
    customer_details_window.attributes("-fullscreen", True)
    
    #Uploading Image
    img=Image.open("images/Services.jpg")
    photoimg=ImageTk.PhotoImage(img)

    img_lbl = tk.Label(customer_details_window, image=photoimg)
    img_lbl.place(x=0,y=0, width=1366, height=768)
    
    img_lbl.image = photoimg

    customer_name_label = tk.Label(customer_details_window, text="Customer Name:", font=("open sans", 15, "bold"), fg="#06392e", bd=0, highlightthickness=0, bg="white")
    customer_name_entry = tk.Entry(customer_details_window, font=("open sans", 15))

    phone_number_label = tk.Label(customer_details_window, text="Phone Number:", font=("open sans", 15, "bold"), fg="#06392e", bd=0, highlightthickness=0, bg="white")
    phone_number_entry = tk.Entry(customer_details_window, font=("open sans", 15))

    email_label = tk.Label(customer_details_window, text="Email:", font=("open sans", 15, "bold"), fg="#06392e", bd=0, highlightthickness=0, bg="white")
    email_entry = tk.Entry(customer_details_window, font=("open sans", 15))

    next_button = tk.Button(customer_details_window, text="Next", font=("open sans", 12, "bold"), fg="white", bd=0, highlightthickness=0, bg="green",command=lambda: show_product_category(customer_name_entry.get(), phone_number_entry.get(), email_entry.get(), bill_number, customer_details_window), cursor="hand2")
    
    customer_name_label.place(relx=0.65, rely=0.3, width=200, height=50, anchor="center")
    customer_name_entry.place(relx=0.82, rely=0.3, width=200, height=50, anchor="center")

    phone_number_label.place(relx=0.65, rely=0.4, width=200, height=50, anchor="center")
    phone_number_entry.place(relx=0.82, rely=0.4, width=200, height=50, anchor="center")

    email_label.place(relx=0.65, rely=0.5, width=200, height=50, anchor="center")
    email_entry.place(relx=0.82, rely=0.5, width=200, height=50, anchor="center")

    next_button.place(relx=0.875, rely=0.57, width=60,height=30,anchor="center")
    
    #clear button
    clear_button = tk.Button(customer_details_window, text="Back", font=("open sans", 15, "bold"), fg="#06392e", command=lambda:exit(customer_details_window), bd=0, highlightthickness=0, bg="white", cursor="hand2")
    clear_button.place(relx=0.24, rely=0.62, width=200, height=50, anchor="center")
#=============================================================================================

# Main GUI setup
root = tk.Tk()
root.geometry("1530x800+0+0")
root.title("Grocery Billing System")

# To see the window in Fullscreen
root.attributes("-fullscreen", True)

# Creating main frame for more control over gui
main_frame = tk.Frame(root, bd=0)
main_frame.place(width=1530, height=800)

#Uploading Image
img=Image.open("images/Services.jpg")
photoimg=ImageTk.PhotoImage(img)

img_lbl = tk.Label(main_frame, image=photoimg)
img_lbl.place(x=0,y=0, width=1366, height=768)

# GUI elements for 1st screen
search_bill_button = tk.Button(main_frame, text="Search", font=("open sans", 15, "bold"), fg="#06392e", command=search_bill, bd=0, highlightthickness=0, bg="white", cursor="hand2")
generate_bill_button = tk.Button(main_frame, text="Generate", font=("open sans", 15, "bold"), fg="#06392e",command=show_customer_details, bd=0, highlightthickness=0, bg="white", cursor="hand2")
clear_button = tk.Button(main_frame, text="Exit", font=("open sans", 12, "bold"), fg="white", command=lambda:exit(root), bd=0, highlightthickness=0, bg="red3", cursor="hand2")
about_us = tk.Button(main_frame, text="About Us", font=("open sans", 12, "bold"), fg="white", command=lambda:info(), bd=0, highlightthickness=0, bg="green", cursor="hand2")


# search_bill_button.place(x=1000,y=400, width=80, height=20)
search_bill_button.place(relx=0.2, rely=0.558, width=200, height=50, anchor="center")
generate_bill_button.place(relx=0.35, rely=0.558, width=200,height=50,anchor="center")
clear_button.place(relx=0.56, rely=0.23, width=80,height=30,anchor="center")
about_us.place(relx=0.5, rely=0.23, width=80,height=30,anchor="center")



# About us showing page function
def info():
    right = tk.LabelFrame(main_frame, text=" ", font=("open sans", 16, "bold"), fg="#06392E", bg="white", bd=0, highlightthickness=0)
    right.place(x=715, y=152, width=380, height=390)
    
    scroll_y = tk.Scrollbar(right, orient="vertical")
    textarea = tk.Text(right, yscrollcommand=scroll_y.set, bg="white", fg="#06392E", bd=0, highlightthickness=0, font=("open sans", 13), wrap=tk.WORD, padx=10,pady=10)
    
    text= """Welcome to this programme, I created this programme for the understanding of simple python GUI. 
    
Here I used tkinter library. 
    
For this project, I have created software that can be used in any shop, supermarket, or even restaurant. 

With its help, we can create receipts for shops, and you can also save the complete data in a MySQL database. 

This is not fully fledged yet, but it shows the implementation of this type of programmes.
    
Click Search to search a bill by bill number or click generate to create a new bill.
    """
    
    textarea.insert(tk.END, text)

    # Make text bold and large
    edit_text(textarea, "Welcome to this programmes, I created this", "or click generate to create a new bill.","open sans", 13)


    
    textarea.config(state="disabled")
    textarea.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")
    
    # Function to close the info frame
    def close_info():
        right.destroy()
        
    close_button = tk.Button(right, text="X", font=("open sans", 12, "bold"), fg="white", command=lambda:close_info(), bd=0, highlightthickness=0, bg="red3", cursor="hand2")
    close_button.place(relx=0.974, rely=-0.05, width=20,height=20,anchor="center")


# Run the Tkinter main loop
root.mainloop()
