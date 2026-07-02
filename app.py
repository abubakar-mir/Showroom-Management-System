from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = 'showroom.db'

# Utility function to get DB connection
def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ------------------ PRODUCTS ------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()

    # Fetch products
    products = conn.execute("""
        SELECT Product.*, Supplier.Name AS SupplierName
        FROM Product
        LEFT JOIN Supplier ON Product.SupplierID = Supplier.SupplierID
    """).fetchall()

    # Fetch suppliers for dropdown
    suppliers = conn.execute(
        "SELECT SupplierID, Name FROM Supplier"
    ).fetchall()

    # Handle form submit
    if request.method == 'POST':
        name = request.form['name']
        model = request.form['model']
        price = request.form['price']
        stock = request.form['stock']
        supplier_id = request.form['supplier_id']

        conn.execute(
            "INSERT INTO Product (Name, Model, Price, Stock, SupplierID) VALUES (?, ?, ?, ?, ?)",
            (name, model, price, stock, supplier_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template(
        'index.html',
        products=products,
        suppliers=suppliers
    )




@app.route('/add-product', methods=['POST'])
def add_product():



    name = request.form['name']
    model = request.form['model']
    price = request.form['price']
    stock = request.form['stock']
    supplier = request.form['supplier_id']

    
    conn = get_db_connection()
    conn.execute('INSERT INTO Product (Name, Model, Price, Stock, SupplierID) VALUES (?, ?, ?, ?, ?)',
                 (name, model, price, stock, supplier))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete-product/<int:id>')
def delete_product(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Product WHERE ProductID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM Product WHERE ProductID = ?", (id,)).fetchone()
    suppliers = conn.execute("SELECT SupplierID, Name FROM Supplier").fetchall()

    if request.method == 'POST':
        name = request.form['name']
        model = request.form['model']
        price = request.form['price']
        stock = request.form['stock']
        supplier_id = request.form['supplier_id']  

        conn.execute("""
            UPDATE Product
            SET Name=?, Model=?, Price=?, Stock=?, SupplierID=?
            WHERE ProductID=?
        """, (name, model, price, stock, supplier_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_product.html', product=product, suppliers=suppliers)


# ------------------ CUSTOMER CRUD ------------------

@app.route('/customers')
def customers():
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM Customer').fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)

@app.route('/add-customer', methods=['POST'])
def add_customer():
    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']
    conn = get_db_connection()
    conn.execute('INSERT INTO Customer (Name, Phone, Address) VALUES (?, ?, ?)',
                 (name, phone, address))
    conn.commit()
    conn.close()
    return redirect(url_for('customers'))

@app.route('/delete-customer/<int:id>')
def delete_customer(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Customer WHERE CustomerID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('customers'))

@app.route('/edit-customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM Customer WHERE CustomerID = ?', (id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        conn.execute('UPDATE Customer SET Name=?, Phone=?, Address=? WHERE CustomerID=?',
                     (name, phone, address, id))
        conn.commit()
        conn.close()
        return redirect(url_for('customers'))
    conn.close()
    return render_template('edit_customer.html', customer=customer)

# ------------------ SUPPLIER CRUD ------------------

@app.route('/suppliers')
def suppliers():
    conn = get_db_connection()
    suppliers = conn.execute('SELECT * FROM Supplier').fetchall()
    conn.close()
    return render_template('suppliers.html', suppliers=suppliers)

@app.route('/add-supplier', methods=['POST'])
def add_supplier():
    name = request.form['name']
    company = request.form['company']
    contact = request.form['contact']
    conn = get_db_connection()
    conn.execute('INSERT INTO Supplier (Name, Company, Contact) VALUES (?, ?, ?)',
                 (name, company, contact))
    conn.commit()
    conn.close()
    return redirect(url_for('suppliers'))

@app.route('/delete-supplier/<int:id>')
def delete_supplier(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Supplier WHERE SupplierID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('suppliers'))

@app.route('/edit-supplier/<int:id>', methods=['GET', 'POST'])
def edit_supplier(id):
    conn = get_db_connection()
    supplier = conn.execute('SELECT * FROM Supplier WHERE SupplierID = ?', (id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        company = request.form['company']
        contact = request.form['contact']
        conn.execute('UPDATE Supplier SET Name=?, Company=?, Contact=? WHERE SupplierID=?',
                     (name, company, contact, id))
        conn.commit()
        conn.close()
        return redirect(url_for('suppliers'))
    conn.close()
    return render_template('edit_supplier.html', supplier=supplier)

# ------------------ EMPLOYEE CRUD ------------------

@app.route('/employees')
def employees():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM Employee').fetchall()
    conn.close()
    return render_template('employees.html', employees=employees)

@app.route('/add-employee', methods=['POST'])
def add_employee():
    name = request.form['name']
    role = request.form['role']
    contact = request.form['contact']
    conn = get_db_connection()
    conn.execute('INSERT INTO Employee (Name, Role, Contact) VALUES (?, ?, ?)',
                 (name, role, contact))
    conn.commit()
    conn.close()
    return redirect(url_for('employees'))

@app.route('/delete-employee/<int:id>')
def delete_employee(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Employee WHERE EmployeeID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('employees'))

@app.route('/edit-employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    conn = get_db_connection()
    employee = conn.execute('SELECT * FROM Employee WHERE EmployeeID = ?', (id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        contact = request.form['contact']
        conn.execute('UPDATE Employee SET Name=?, Role=?, Contact=? WHERE EmployeeID=?',
                     (name, role, contact, id))
        conn.commit()
        conn.close()
        return redirect(url_for('employees'))
    conn.close()
    return render_template('edit_employee.html', employee=employee)

# ------------------ SALE & PAYMENT ------------------

@app.route('/sales')
def sales():
    conn = get_db_connection()
    sales = conn.execute('''
        SELECT s.SaleID, s.SaleDate, c.Name AS CustomerName, e.Name AS EmployeeName
        FROM Sale s
        JOIN Customer c ON s.CustomerID = c.CustomerID
        JOIN Employee e ON s.EmployeeID = e.EmployeeID
    ''').fetchall()
    conn.close()
    return render_template('sales.html', sales=sales)

@app.route('/add-sale', methods=['GET', 'POST'])
def add_sale():
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM Customer').fetchall()
    employees = conn.execute('SELECT * FROM Employee').fetchall()
    products = conn.execute('SELECT * FROM Product').fetchall()
    
    if request.method == 'POST':
        customer_id = request.form['customer']
        employee_id = request.form['employee']
        sale_date = request.form['sale_date']
        product_ids = request.form.getlist('product')
        quantities = request.form.getlist('quantity')
        
        cur = conn.cursor()
        cur.execute('INSERT INTO Sale (SaleDate, CustomerID, EmployeeID) VALUES (?, ?, ?)',
                    (sale_date, customer_id, employee_id))
        sale_id = cur.lastrowid
        
        for pid, qty in zip(product_ids, quantities):
            price = conn.execute('SELECT Price FROM Product WHERE ProductID=?', (pid,)).fetchone()['Price']
            cur.execute('INSERT INTO SaleDetails (SaleID, ProductID, Quantity, Price) VALUES (?, ?, ?, ?)',
                        (sale_id, pid, qty, price))
        
        conn.commit()
        conn.close()
        return redirect(url_for('sales'))
    
    conn.close()
    return render_template('add_sale.html', customers=customers, employees=employees, products=products)

@app.route('/payments')
def payments():
    conn = get_db_connection()
    payments = conn.execute('''
        SELECT p.PaymentID, s.SaleID, p.Amount, p.PaymentMethod, p.PaymentDate
        FROM Payment p
        JOIN Sale s ON p.SaleID = s.SaleID
    ''').fetchall()
    conn.close()
    return render_template('payments.html', payments=payments)

@app.route('/add-payment', methods=['GET', 'POST'])
def add_payment():
    conn = get_db_connection()
    sales = conn.execute('SELECT * FROM Sale').fetchall()
    if request.method == 'POST':
        sale_id = request.form['sale']
        amount = request.form['amount']
        method = request.form['method']
        date = request.form['date']
        conn.execute('INSERT INTO Payment (SaleID, Amount, PaymentMethod, PaymentDate) VALUES (?, ?, ?, ?)',
                     (sale_id, amount, method, date))
        conn.commit()
        conn.close()
        return redirect(url_for('payments'))
    conn.close()
    return render_template('add_payment.html', sales=sales)

# ------------------ RUN APP ------------------

if __name__ == '__main__':
    app.run(debug=True)
