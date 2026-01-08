Orders Management Application

## Přehled

Orders Management Application je konzolová aplikace pro správu objednávek, zákazníků a produktů. Aplikace používá Python 3 a MySQL a je připravena pro rychlý start s připravenou databází.

## Konfigurace

Aplikace používá soubor `app_config.ini` pro nastavení databáze a informací o aplikaci.

[database]
host = localhost

port = 3306

database = orders_management

user = root

password = password


[application]
name = OrdersManagementApplication
version = 1.0.0

## Spuštění aplikace

1. Ujistěte se, že máte nainstalovaný Python 3 a MySQL.
   
2. Nastavte si `user` a `password` v `app_config.ini`.

3. (Optional) Naimportujte svůj soubor s daty do složky data a smažte vše co je v RDMS_project/sql/sample_data.sql 

## Import vlastních dat
* Zákazníci: CSV soubor s poli first_name, last_name, email, phone.
* Produkty: JSON soubor s poli name, description, price, stock_quantity.

vzor pro generování dat:

-- produkty JSON
  {
    "name": "Laptop",
    "description": "15-inch business laptop",
    "price": 1200.00,
    "stock_quantity": 10
  }

-- zákazníci CSV
first_name,last_name,email,phone
John,Doe,john.doe@example.com,+420111222333


4. Spuštění aplikace:

python main.py

## Použité návrhové vzory

* DAO (CustomerDAO, ProductRepository)
* Repository / Service Layer
