# Showroom Management System

A robust, production-ready Vehicle Showroom Management application built to handle complex dealership workflows. This application replaces manual invoicing and stock logs with a relational database backend and an interactive web control dashboard to supervise inventory, manage staff, update customer accounts, and track multi-item transactions.

## 🚀 Key Features

- **Relational Stock Control:** Full CRUD operations for vehicle assets linked directly to wholesaling suppliers.
- **Transactional Invoicing System:** Multi-item purchases are broken down through an associative junction table (`SaleDetails`), capturing exact timestamps, serving staff, and historical unit prices seamlessly.
- **Financial Ledgering:** Tracks settling accounts via an isolated `Payment` table tied to direct sales context to support tracking multiple payout methods (Cash, Card, Bank).
- **Modern Administrative UI:** Styled using responsive tables, clean form components, and a persistent, intuitive dashboard navigation architecture.

## 🛠️ Tech Stack

- **Backend Logic:** Python 3, Flask Framework[cite: 1]
- **Database Engine:** SQLite3 (Native driver connection states)[cite: 1]
- **Frontend Layer:** HTML5, CSS3, Jinja2 Template Engine[cite: 3, 14]

## 📊 Database Architecture

The data layout utilizes an itemized relational model optimized for tracking premium inventory sales seamlessly without record duplication:

- **Customer / Employee / Supplier:** Independent baseline tables capturing unique entity data.
- **Product:** 1-to-Many dependency mapping assets to their original `SupplierID`.
- **Sale & SaleDetails:** Structured via an associative entity strategy to manage variable items per transaction invoice without data duplication.
- **Payment:** Enforces a strict 1-to-1 processing relationship against unique `SaleID` invoices.

### Database Schema Script (`schema.sql`)

```sql
-- 1. Customer Profiles
CREATE TABLE Customer (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Phone TEXT,
    Address TEXT
);

-- 2. Showroom Staff Records
CREATE TABLE Employee (
    EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Role TEXT,
    Contact TEXT
);

-- 3. Inventory Wholesalers / Suppliers
CREATE TABLE Supplier (
    SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Company TEXT,
    Contact TEXT
);

-- 4. Vehicle Inventory Table
CREATE TABLE Product (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Model TEXT,
    Price REAL NOT NULL,
    Stock INTEGER,
    SupplierID INTEGER,
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

-- 5. Master Sales Transactions Log
CREATE TABLE Sale (
    SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
    SaleDate TEXT NOT NULL,
    CustomerID INTEGER NOT NULL,
    EmployeeID INTEGER NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

-- 6. Itemized Sales Junction Table (Handles Multi-Vehicle Invoices)
CREATE TABLE SaleDetails (
    SaleDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
    SaleID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    Price REAL,
    FOREIGN KEY (SaleID) REFERENCES Sale(SaleID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

-- 7. Payment Ledger tracking financial settling
CREATE TABLE Payment (
    PaymentID INTEGER PRIMARY KEY AUTOINCREMENT,
    SaleID INTEGER NOT NULL UNIQUE,
    Amount REAL NOT NULL,
    PaymentMethod TEXT,
    PaymentDate TEXT NOT NULL,
    FOREIGN KEY (SaleID) REFERENCES Sale(SaleID)
);
