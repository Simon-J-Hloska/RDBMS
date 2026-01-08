from RDBMS_project.src.model.customer import Customer
from RDBMS_project.src.ui.user_interface import UserInterface
from RDBMS_project.src.service.customer_service import CustomerService
from RDBMS_project.src.service.order_service import OrderService
from RDBMS_project.src.service.report_service import ReportService
from RDBMS_project.src.service.import_service import ImportService
from RDBMS_project.src.repository.product_repository import ProductRepository
from RDBMS_project.src.model.product import Product
from RDBMS_project.src.utils.error_handler import ErrorHandler
from RDBMS_project.src.dao.customer_dao import CustomerDAO


class MenuController:
    def __init__(self):
        self.ui = UserInterface()
        self.customer_service = CustomerService()
        self.order_service = OrderService()
        self.report_service = ReportService()
        self.import_service = ImportService()
        self.product_repository = ProductRepository()
        self.dao = CustomerDAO()

    def run(self):
        """
        shows the main menu with all features
        :return: None
        """
        while True:
            self.ui.clear_screen()
            self.ui.print_header("SYSTÉM SPRÁVY OBJEDNÁVEK")
            print("1. Správa zákazníků")
            print("2. Správa produktů")
            print("3. Správa objednávek")
            print("4. Reporty")
            print("5. Import dat")
            print("0. Ukončit")

            choice = self.ui.get_input("\nVyberte možnost")

            if choice == '1':
                self.customer_menu()
            elif choice == '2':
                self.product_menu()
            elif choice == '3':
                self.order_menu()
            elif choice == '4':
                self.report_menu()
            elif choice == '5':
                self.import_menu()
            elif choice == '0':
                print("\nNa shledanou!\n")
                break

    def customer_menu(self):
        """
        shows a menu for Customer management
        :return: None
        """
        while True:
            self.ui.clear_screen()
            self.ui.print_header("SPRÁVA ZÁKAZNÍKŮ")
            print("1. Vytvořit zákazníka")
            print("2. Zobrazit všechny zákazníky")
            print("3. Vyhledat zákazníka")
            print("4. Upravit zákazníka")
            print("5. Smazat zákazníka")
            print("0. Zpět")

            choice = self.ui.get_input("\nVyberte možnost")

            if choice == '1':
                self.create_customer()
            elif choice == '2':
                self.list_customers()
            elif choice == '3':
                self.find_customer()
            elif choice == '4':
                self.update_customer()
            elif choice == '5':
                self.delete_customer()
            elif choice == '0':
                break

    def order_menu(self):
        """
        shows a menu for order manipulations
        :return: None
        """
        while True:
            self.ui.clear_screen()
            self.ui.print_header("SPRÁVA OBJEDNÁVEK")
            print("1. Vytvořit objednávku")
            print("2. Zobrazit objednávku")
            print("3. Změnit stav objednávky")
            print("4. Zrušit objednávku")
            print("5. Zobrazit všechny objednávky")
            print("0. Zpět")

            choice = self.ui.get_input("\nVyberte možnost")

            if choice == '1':
                self.create_order()
            elif choice == '2':
                self.view_order()
            elif choice == '3':
                self.update_order_status()
            elif choice == '4':
                self.cancel_order()
            elif choice == '5':
                self.list_orders()
            elif choice == '0':
                break

    def cancel_order(self):
        """
        Cancels the creation of a new order by id
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("ZRUŠIT OBJEDNÁVKU")

        try:
            order_id = self.ui.get_integer_input("ID objednávky")
            if not order_id:
                return

            if self.ui.confirm("Opravdu chcete zrušit tuto objednávku?"):
                self.order_service.cancel_order(order_id)
                self.ui.print_success("Objednávka zrušena")

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def list_orders(self):
        """
        lists all orders made
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("SEZNAM OBJEDNÁVEK")

        try:
            orders = self.order_service.get_all_orders()
            if not orders:
                self.ui.print_info("Žádné objednávky")
            else:
                headers = ["ID", "Zákazník", "Datum", "Stav", "Celkem"]
                rows = [
                    [o.order_id, o.customer_id, o.order_date, o.status, o.total_amount]
                    for o in orders
                ]
                self.ui.print_table(headers, rows)

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def create_order(self):
        """
        Creates an order through DAO
        :return:
        """
        self.ui.clear_screen()
        self.ui.print_header("NOVÁ OBJEDNÁVKA")

        try:
            customer_id = self.ui.get_integer_input("ID zákazníka")
            if not customer_id:
                return

            items = []
            while True:
                product_id = self.ui.get_integer_input("ID produktu (0 => konec)")
                if not product_id:
                    break

                quantity = self.ui.get_integer_input("Množství")
                if quantity:
                    items.append((product_id, quantity))

            payment_method = self.ui.get_input("Platební metoda")

            order_id = self.order_service.create_order(
                customer_id=customer_id,
                items=items,
                payment_method=payment_method
            )

            self.ui.print_success(f"Objednávka vytvořena (ID: {order_id})")

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def report_menu(self):
        """
        creates a menu of reports
        :return: None
        """
        while True:
            self.ui.clear_screen()
            self.ui.print_header("REPORTY")
            print("1. Přehled prodejů")
            print("2. Produkty s nízkým stavem zásob")
            print("3. Statistiky zákazníka")
            print("0. Zpět")

            choice = self.ui.get_input("\nVyberte možnost")

            if choice == '1':
                self.sales_summary_report()
            elif choice == '2':
                self.low_stock_report()
            elif choice == '3':
                self.customer_statistics_report()
            elif choice == '0':
                break

    def sales_summary_report(self):
        """
        generates sales report
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("PŘEHLED PRODEJŮ")

        try:
            summary = self.report_service.get_sales_summary()

            headers = ["Ukazatel", "Hodnota"]
            rows = [
                ["Celkem objednávek", summary['total_orders']],
                ["Dokončené objednávky", summary['completed_orders']],
                ["Čekající objednávky", summary['pending_orders']],
                ["Celkový obrat", summary['total_revenue']]
            ]

            self.ui.print_table(headers, rows)

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def low_stock_report(self):
        """
        generates a report if there's a shortage
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("PRODUKTY S NÍZKÝM STAVEM ZÁSOB")

        try:
            threshold = self.ui.get_integer_input(
                "Limit zásob (výchozí 10)"
            ) or 10

            products = self.report_service.get_low_stock_products(threshold)

            if not products:
                self.ui.print_info("Žádné produkty pod stanoveným limitem")
            else:
                headers = ["ID", "Název", "Skladem"]
                rows = [
                    [p.product_id, p.name, p.stock_quantity]
                    for p in products
                ]
                self.ui.print_table(headers, rows)

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def customer_statistics_report(self):
        """
        Shows the statistics of a customer found by id
        :return:
        """
        self.ui.clear_screen()
        self.ui.print_header("STATISTIKY ZÁKAZNÍKA")

        try:
            customer_id = self.ui.get_integer_input("ID zákazníka")
            if not customer_id:
                return

            stats = self.report_service.get_customer_statistics(customer_id)

            headers = ["Ukazatel", "Hodnota"]
            rows = [
                ["Celkem objednávek", stats['total_orders']],
                ["Dokončené objednávky", stats['completed_orders']],
                ["Celkem utraceno", stats['total_spent']]
            ]

            self.ui.print_table(headers, rows)

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def update_order_status(self):
        """
        updates the order status
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("ZMĚNIT STAV OBJEDNÁVKY")

        try:
            order_id = self.ui.get_integer_input("ID objednávky")
            if not order_id:
                return

            status = self.ui.get_input(
                "Nový stav (pending/confirmed/shipped/delivered/cancelled)"
            )

            self.order_service.update_order_status(order_id, status)
            self.ui.print_success("Stav objednávky aktualizován")

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def view_order(self):
        """
        Shows the order that was looked up by ID
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("ZOBRAZIT OBJEDNÁVKU")

        try:
            order_id = self.ui.get_integer_input("ID objednávky")
            if not order_id:
                return

            order = self.order_service.get_order(order_id)
            if not order:
                self.ui.print_info("Objednávka nenalezena")
            else:
                print(f"\nID: {order.order_id}")
                print(f"Zákazník: {order.customer_id}")
                print(f"Datum: {order.order_date}")
                print(f"Stav: {order.status}")
                print(f"Celkem: {order.total_amount}")

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def import_menu(self):
        """
        Menu for importing products or products
        :return: None
        """
        while True:
            self.ui.clear_screen()
            self.ui.print_header("IMPORT DAT")
            print("1. Import zákazníků z CSV")
            print("2. Import produktů z JSON")
            print("0. Zpět")

            choice = self.ui.get_input("\nVyberte možnost")

            if choice == '1':
                self.import_customers()
            elif choice == '2':
                self.import_products()
            elif choice == '0':
                break

    def import_customers(self):
        """
        Imports customers from CSV
        :return:
        """
        self.ui.clear_screen()
        self.ui.print_header("IMPORT ZÁKAZNÍKŮ (CSV)")

        try:
            file_path = self.ui.get_input("Cesta k CSV souboru")
            if not file_path:
                return

            count = self.import_service.import_customers_from_csv(file_path)
            self.ui.print_success(f"Importováno zákazníků: {count}")

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def import_products(self):
        """
        imports products from JSON
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("IMPORT PRODUKTŮ (JSON)")

        try:
            file_path = self.ui.get_input("Cesta k JSON souboru")
            if not file_path:
                return

            count = self.import_service.import_products_from_json(file_path)
            self.ui.print_success(f"Importováno produktů: {count}")

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def create_customer(self):
        """
        creates a customer object
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("NOVÝ ZÁKAZNÍK")

        try:
            first_name = self.ui.get_input("Jméno")
            last_name = self.ui.get_input("Příjmení")
            email = self.ui.get_input("Email")
            phone = self.ui.get_input("Telefon")

            customer_id = self.customer_service.create_customer(
                first_name, last_name, email, phone
            )
            self.ui.print_success(f"Zákazník vytvořen s ID: {customer_id}")
        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def list_customers(self):
        """
        lists customers
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("SEZNAM ZÁKAZNÍKŮ")

        try:
            customers = self.customer_service.get_all_customers()

            if not customers:
                self.ui.print_info("Žádní zákazníci nenalezeni")
            else:
                headers = ["ID", "Jméno", "Příjmení", "Email", "Telefon"]
                rows = [[c.customer_id, c.first_name, c.last_name, c.email, c.phone]
                        for c in customers]
                self.ui.print_table(headers, rows)
        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def find_customer(self):
        """
        finds a customer by ID
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("VYHLEDAT ZÁKAZNÍKA")

        try:
            customer_id = self.ui.get_integer_input("ID zákazníka")
            if customer_id:
                customer = self.customer_service.get_customer(customer_id)
                if customer:
                    print(f"\nID: {customer.customer_id}")
                    print(f"Jméno: {customer.first_name} {customer.last_name}")
                    print(f"Email: {customer.email}")
                    print(f"Telefon: {customer.phone}")
                    print(f"Vytvořeno: {customer.created_at}")
                else:
                    self.ui.print_info("Zákazník nenalezen")
        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def update_customer(self):
        """
        updates customer info
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("UPRAVIT ZÁKAZNÍKA")

        try:
            customer_id = self.ui.get_integer_input("ID zákazníka")
            if not customer_id:
                return

            customer = self.customer_service.get_customer(customer_id)
            if not customer:
                self.ui.print_info("Zákazník nenalezen")
                self.ui.pause()
                return

            print(f"\nAktuální údaje:")
            print(f"Jméno: {customer.first_name}")
            print(f"Příjmení: {customer.last_name}")
            print(f"Email: {customer.email}")
            print(f"Telefon: {customer.phone}\n")

            first_name = self.ui.get_input("Nové jméno")
            last_name = self.ui.get_input("Nové příjmení")
            email = self.ui.get_input("Nový email")
            phone = self.ui.get_input("Nový telefon")

            self.customer_service.update_customer(
                customer_id, first_name, last_name, email, phone
            )
            self.ui.print_success("Zákazník upraven")
        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def delete_customer(self):
        """
        deletes the customer by id
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("SMAZAT ZÁKAZNÍKA")

        try:
            customer_id = self.ui.get_integer_input("ID zákazníka")
            if not customer_id:
                return

            if self.ui.confirm("Opravdu chcete smazat tohoto zákazníka?"):
                self.delete(customer_id)
                self.ui.print_success("Zákazník smazán")
        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def product_menu(self):
        """
        shows the product menu
        :return: None
        """
        while True:
            self.ui.clear_screen()
            self.ui.print_header("SPRÁVA PRODUKTŮ")
            print("1. Přidat produkt")
            print("2. Zobrazit všechny produkty")
            print("3. Vyhledat produkt")
            print("4. Upravit produkt")
            print("5. Smazat produkt")
            print("0. Zpět")

            choice = self.ui.get_input("\nVyberte možnost")

            if choice == '1':
                self.create_product()
            elif choice == '2':
                self.list_products()
            elif choice == '3':
                self.find_product()
            elif choice == '4':
                self.update_product()
            elif choice == '5':
                self.delete_product()
            elif choice == '0':
                break

    def delete_product(self):
        """
        deletes the product
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("SMAZAT PRODUKT")

        try:
            product_id = self.ui.get_integer_input("ID produktu")
            if not product_id:
                return

            product = self.product_repository.find_by_id(product_id)
            if not product:
                self.ui.print_info("Produkt nenalezen")
                self.ui.pause()
                return

            if self.ui.confirm(f"Opravdu chcete smazat produkt '{product.name}'?"):
                self.product_repository.delete(product_id)
                self.ui.print_success("Produkt smazán")

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def find_product(self):
        """
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("VYHLEDAT PRODUKT")

        try:
            product_id = self.ui.get_integer_input("ID produktu")
            if not product_id:
                return

            product = self.product_repository.find_by_id(product_id)
            if product:
                print(f"\nID: {product.product_id}")
                print(f"Název: {product.name}")
                print(f"Popis: {product.description}")
                print(f"Cena: {product.price}")
                print(f"Sklad: {product.stock_quantity}")
                print(f"Vytvořeno: {product.created_at}")
            else:
                self.ui.print_info("Produkt nenalezen")

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def update_product(self):
        """
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("UPRAVIT PRODUKT")

        try:
            product_id = self.ui.get_integer_input("ID produktu")
            if not product_id:
                return

            product = self.product_repository.find_by_id(product_id)
            if not product:
                self.ui.print_info("Produkt nenalezen")
                self.ui.pause()
                return

            print("\nAktuální údaje:")
            print(f"Název: {product.name}")
            print(f"Popis: {product.description}")
            print(f"Cena: {product.price}")
            print(f"Sklad: {product.stock_quantity}\n")

            name = self.ui.get_input("Nový název")
            description = self.ui.get_input("Nový popis")
            price = self.ui.get_number_input("Nová cena")
            stock = self.ui.get_integer_input("Nové množství")

            product.name = name or product.name
            product.description = description or product.description
            product.price = price if price is not None else product.price
            product.stock_quantity = stock if stock is not None else product.stock_quantity

            self.product_repository.update(product)
            self.ui.print_success("Produkt upraven")

        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def create_product(self):
        """
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("NOVÝ PRODUKT")

        try:
            name = self.ui.get_input("Název")
            description = self.ui.get_input("Popis")
            price = self.ui.get_number_input("Cena")
            stock = self.ui.get_integer_input("Množství na skladě")

            if price and stock:
                product = Product(
                    name=name,
                    description=description,
                    price=price,
                    stock_quantity=stock
                )
                product_id = self.product_repository.save(product)
                self.ui.print_success(f"Produkt vytvořen s ID: {product_id}")
        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def list_products(self):
        """
        prints the list of products
        :return: None
        """
        self.ui.clear_screen()
        self.ui.print_header("SEZNAM PRODUKTŮ")

        try:
            products = self.product_repository.find_all()

            if not products:
                self.ui.print_info("Žádný produkt v DB")
            else:
                headers = ["ID", "Název", "Popis", "Cena", "Sklad"]
                rows = [
                    [
                        p.product_id,
                        p.name,
                        p.description,
                        p.price,
                        p.stock_quantity
                    ]
                    for p in products
                ]
                self.ui.print_table(headers, rows)
        except Exception as e:
            self.ui.print_error(ErrorHandler.handle_exception(e))

        self.ui.pause()

    def update(self, customer):
        """
        updates the customer obj passed in
        :param customer: Customer object
        :return: Number of affected rows
        """
        return self.dao.update(
            customer.customer_id,
            customer.first_name,
            customer.last_name,
            customer.email,
            customer.phone
        )

    def delete(self, customer_id):
        """
        :param customer_id: Customer ID
        :return: Number of affected rows
        """
        return self.dao.delete(customer_id)

    def find_by_email(self, email):
        """
        :param email: Customer email
        :return: Customer object or None
        """
        data = self.dao.find_by_email(email)
        if data:
            return Customer(
                customer_id=data[0],
                first_name=data[1],
                last_name=data[2],
                email=data[3],
                phone=data[4],
                created_at=data[5]
            )
        return None

