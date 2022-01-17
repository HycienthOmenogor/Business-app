import sqlite3
from datetime import date
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry

conn = sqlite3.connect('drinks.sqlite')

cursor = conn.cursor()

#Create tables 
"""
cursor.executescript('''
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Purchase;
DROP TABLE IF EXISTS Sales;
    
CREATE TABLE Products(
    'Product name' TEXT NOT NULL
    );

CREATE TABLE Purchase(
    Date INTEGER,
    'Product name' TEXT NOT NULL,
    'Quantity bought' INTEGER,
    'Unit price' INTEGER,
    'Total price' INTEGER
    );

CREATE TABLE Sales(
    Date INTEGER,
    'Product name' TEXT NOT NULL,
    'Quantity sold' INTEGER,
    Price INTEGER,
    'Total price' INTEGER
    )
    ''')
"""
root = Tk()
root.title('Menu')
root.geometry('150x100')

#List of produts
prod_list = ['35cl pet','35cl RGB','50cl RGB','60cl pet','7up(60cl)','7up(RGB)',
    'Algor water(50cl)','Algor water(75cl)','Amstel malt','Berryblast',
    'Bigi cola','Capri-sun','Coke(can)','Dubic malt','Eva(big)','Eva(small)',
    'Fayrouz','Fearless','Five Alive(big)','Five Alive(Black)',
    'Five Alive(small)','Ginger','Ginger bold','Goldberg','Hero',
    'Ice block(big)','Ice block(small)','Lacasera(big)','Lacasera(small)',
    'Limca','Malta Guiness(RGB)','Malta Guinness(can)','Maltina','Nutri choco',
    'Nutri milk(big)','Nutri milk(small)','Nutri yo','Pepsi(pet)','Pepsi(RGB)',
    'Predator','Schwepps(can)','Schwepps(pet)','Schwepps(RGB)','Smoove',
    'Sprite(can)','Teem soda','Zero coke','Zobo']

#Create A Sales GUI
def sales_func():
    root = Tk()
    root.title('SALES RECORD')
    root.geometry('600x400')
    #root.configure(background='#676665')

    def sales_submit():
        date_format = date.get_date().strftime('%d/%m/%Y')
        prod_name = mycombo.get()
        qty_sold = int(quantity.get())
        unit_price = int(price.get())
        price_calc = int(qty_sold * unit_price)
        cursor.execute('INSERT OR IGNORE INTO Sales VALUES (?,?,?,?,?)', 
        (date_format, prod_name, qty_sold, unit_price, price_calc))
    
        #Clear text boxes after action is completed
        #date.delete(0, END)
        #product.delete(0, END)
        #quantity.delete(0, END)
        #price.delete(0, END)
        #total_price.delete(0, END)

        price_total_label=Label(root, text=price_calc)
        price_total_label.grid(row=4, column=1)

        conn.commit()

    def sales_query():
        root_sale = Tk()
        root_sale.title('LIST OF SALES')
        root_sale.geometry('500x600')


        cursor.execute('SELECT *, oid FROM Sales')
        records = cursor.fetchall()
        record_list =''
        for record in records:
            record_list += str(record) + '\n'

        def close():
            root_sale.destroy()

        def sales_delete():
            id = select_label_entry.get()
            cursor.execute('DELETE FROM Sales WHERE oid = ?', (id,))
            conn.commit()

            #Clear entry box after delete operation
            select_label_entry.delete(0, END)
    
        root_sale.update()
    
        sales_query_label = Label(root_sale, text = record_list)
        sales_query_label.grid(row=0, column=0, pady=10)

        action_frame = Frame(root_sale)
        action_frame.grid(row=1, column=0, pady=10)

        select_label = Label(action_frame, text='Select ID')
        select_label.grid(row=0, column=0, rowspan=2, pady=10)

        select_label_entry = Entry(action_frame, width=10)
        select_label_entry.grid(row=0, column=1, rowspan=2, pady=10)

        delete_btn = Button(action_frame, text='Delete', command = sales_delete)
        delete_btn.grid(row=0, column=2, rowspan=2, pady=10, padx=10)

        close_btn = Button(root_sale, text='CLOSE', command = close)
        close_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10, ipadx=120)


    #Create textbox label
    product_label = Label(root, text='Product name')
    product_label.grid(row=0, column=0, pady=(10, 0))
    date_label = Label(root, text='Date')
    date_label.grid(row=1, column=0)
    quantity_label = Label(root, text='Quantity sold')
    quantity_label.grid(row=2, column=0)
    price_label = Label(root, text='Price')
    price_label.grid(row=3, column=0)
    total_price_label = Label(root, text='Total price')
    total_price_label.grid(row=4, column=0)

    #Create textboxes
    product = Entry(root, width=20)
    product.grid(row=0, column=1, columnspan=2, pady=(10, 0))
    date = DateEntry(root, width=18, pady=10, background='blue',
            foreground='red')
    date.grid(row=1, column=1)
    date._top_cal.overrideredirect(False)

    quantity = Entry(root, width=20)
    quantity.grid(row=2, column=1)
    price = Entry(root, width=20)
    price.grid(row=3, column=1)

    #Create buttons
    submit_btn = Button(root, text='Submit', command = sales_submit)
    submit_btn.grid(row=5, column=0, pady=20, padx=20)

    show_btn = Button(root, text='Show Records', command = sales_query)
    show_btn.grid(row=5, column=1, pady=20, padx=10)


    #create a combobox
    mycombo = ttk.Combobox(root, value=prod_list)
    #mycombo.current(0)
    mycombo.bind('<<ComboboxSelected>>')
    mycombo.grid(row=0, column=1, columnspan=2, pady=(10, 0))


    root.mainloop()

############################################################################
#Create a purchase GUI
def purchase_func():
    rootp = Tk()
    rootp.title('PURCHASE RECORDS')
    rootp.geometry('650x400')

    def purchase_submit():
        date_format = date.get_date().strftime('%d/%m/%Y')
        prod_name = mycombo.get()
        qty_purchased = int(quantity.get())
        unit_price = int(price.get())
        price_calc = int(qty_purchased * unit_price)
        cursor.execute('INSERT OR IGNORE INTO Purchase VALUES (?,?,?,?,?)', 
        (date_format, prod_name, qty_purchased, unit_price, price_calc))
 
        price_total_label=Label(rootp, text=price_calc)
        price_total_label.grid(row=4, column=1)

        conn.commit()

 
    def purchase_query():
        rootp_purchase = Tk()
        rootp_purchase.title('LIST OF PURCHASE')
        rootp_purchase.geometry('500x600')


        cursor.execute('SELECT *, oid FROM Purchase')
        records = cursor.fetchall()
        record_list =''
        for record in records:
            record_list += str(record) + '\n'


        def close():
            rootp_purchase.destroy()

        def purchase_delete():
            id = select_label_entry.get()
            cursor.execute('DELETE FROM Purchase WHERE oid = ?', (id,))
            conn.commit()

            #Clear entry box after delete operation
            select_label_entry.delete(0, END)
    
        rootp_purchase.update()
    
        purchase_query_label = Label(rootp_purchase, text = record_list)
        purchase_query_label.grid(row=0, column=0, pady=10)

        action_frame = Frame(rootp_purchase)
        action_frame.grid(row=1, column=0, pady=10)

        select_label = Label(action_frame, text='Select ID')
        select_label.grid(row=0, column=0, rowspan=2, pady=10)

        select_label_entry = Entry(action_frame, width=10)
        select_label_entry.grid(row=0, column=1, rowspan=2, pady=10)

        delete_btn = Button(action_frame, text='Delete',
            command = purchase_delete)
        delete_btn.grid(row=0, column=2, rowspan=2, pady=10, padx=10)

        close_btn = Button(rootp_purchase, text='CLOSE', command = close)
        close_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10,
            ipadx=120)


    #Create textbox label
    product_label = Label(rootp, text='Product name')
    product_label.grid(row=0, column=0, pady=(10, 0))
    date_label = Label(rootp, text='Date')
    date_label.grid(row=1, column=0)
    quantity_label = Label(rootp, text='Quantity purchased')
    quantity_label.grid(row=2, column=0)
    price_label = Label(rootp, text='Price')
    price_label.grid(row=3, column=0)
    total_price_label = Label(rootp, text='Total price')
    total_price_label.grid(row=4, column=0)

    #Create textboxes
    product = Entry(rootp, width=20)
    product.grid(row=0, column=1, columnspan=2, pady=(10, 0))
    date = DateEntry(rootp, width=18, pady=10, background='blue',
        foreground='red')
    date.grid(row=1, column=1)
    date._top_cal.overrideredirect(False)
    quantity = Entry(rootp, width=20)
    quantity.grid(row=2, column=1)
    price = Entry(rootp, width=20)
    price.grid(row=3, column=1)

    #Create buttons
    submit_btn = Button(rootp, text='Submit', command = purchase_submit)
    submit_btn.grid(row=5, column=0, pady=20, padx=20)

    show_btn = Button(rootp, text='Show Records', command = purchase_query)
    show_btn.grid(row=5, column=1, pady=20, padx=10)


    #create a combobox
    mycombo = ttk.Combobox(rootp, value=prod_list)
    #mycombo.current(0)
    mycombo.bind('<<Comboboxselected>>')
    mycombo.grid(row=0, column=1, columnspan=2, pady=(10, 0))
 

btn1 = Button(root, text='Sales', command=sales_func, foreground='red')
btn2 = Button(root, text='Purchase', command=purchase_func, foreground='blue')
btn1.pack(padx=10, pady=10)
btn2.pack(padx=10, pady=10)

root.mainloop()
