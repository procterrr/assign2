class Ebook:
    """this is class it will represent an ebook for the ebook store management system."""

    def __init__(self, title, author, publication_date, genre, price):
        """this will initialize a new e-book with given details"""
        self._title = title
        self._author = author
        self._publication_date = publication_date
        self._genre = genre
        self._price = price

    def get_details(self):
        """this will return a sting containing the details of the e-book"""
        return f"Title: {self._title}, Author: {self._author}, " \
               f"Publication Date: {self._publication_date}, Genre: {self._genre}, Price: {self._price:.2f}"

    def __str__(self):
        return self.get_details()

    # getter and setter for each attribute

class Customer:
    """class to represent the customer in the e-bookstore managing system"""
    def __init__(self, name, contact_info, is_loyalty_member=False):
        """this initializes a new customer with given details"""
        self._name = name
        self._contact_info = contact_info
        self._is_loyalty_member = is_loyalty_member

    def apply_loyalty_discount(self, price):
        """applying a loyalty discount if customer is a loyalty member"""
        if self._is_loyalty_member:
            return price * 0.9 # 10% discount
        return price

    def __str__(self):
        return f"Customer: {self._name}. Contact: {self._contact_info}, Loyalty Member: {self._is_loyalty_member}"


class ShoppingCart:
    """Class to manage items in the shopping cart."""

    def __init__(self, customer):
        self._customer = customer
        self._items = []

    def add_item(self, ebook):
        """Add an e-book to the cart."""
        self._items.append(ebook)

    def remove_item(self, ebook):
        """Remove an e-book from the cart."""
        if ebook in self._items:
            self._items.remove(ebook)

    def calculate_total(self):
        """Calculate the total cost of items in the cart, applying discounts."""
        total_before_discount = sum(item._price for item in self._items)

        # Apply loyalty discount if applicable
        total_after_loyalty_discount = self._customer.apply_loyalty_discount(total_before_discount)

        # Apply bulk discount if 5 or more items in the cart
        if len(self._items) >= 5:
            total_after_all_discounts = total_after_loyalty_discount * 0.8  # 20% discount
        else:
            total_after_all_discounts = total_after_loyalty_discount

        return total_before_discount, total_after_all_discounts  # Return both values


    def __str__(self):
        item_details = [item.get_details() for item in self._items]
        return "\n".join(item_details)


from datetime import date

class Order:
    """Class to represent an order."""

    def __init__(self, shopping_cart):
        self._shopping_cart = shopping_cart
        self._order_date = date.today()
        self._total_before_discount, self._total_after_discount = self._shopping_cart.calculate_total()

    def generate_invoice(self):
        """Generates an invoice for the order."""
        return Invoice(self)

    def __str__(self):
        return (f"Order Date: {self._order_date}, "
                f"Total Before Discount: AED {self._total_before_discount:.2f}, "
                f"Total After Discount: AED {self._total_after_discount:.2f}")

class Invoice:
    """Class to represent an invoice for an order."""

    VAT_RATE = 0.08  # 8% VAT rate

    def __init__(self, order):
        self._order = order
        self._total_before_tax = order._total_after_discount
        self._vat = self._total_before_tax * self.VAT_RATE
        self._total_after_tax = self._total_before_tax + self._vat

    def __str__(self):
        return (f"Invoice:\n"
                f"Total Before Tax: AED {self._total_before_tax:.2f}\n"
                f"VAT (8%): AED {self._vat:.2f}\n"
                f"Total After Tax: AED {self._total_after_tax:.2f}")

class DiscountManager:
    """
    class to manage discounts in the E-Bookstore management system.
    """

    LOYALTY_DISCOUNT = 0.1 # 10% discount
    BULK_DISCOUNT = 0.2 # 20%  discount for 5 or more e-books

    def apply_loyalty_discount(self, price, is_loyalty_member):
        """applies a loyalty discount to the price"""
        if is_loyalty_member:
            return price * (1 - self.LOYALTY_DISCOUNT)
        return price

    def apply_bulk_discount(self, price, quantity):
        """applies a bulk discount to the price if quantity is 5 or more."""
        if quantity >= 5:
            return price * (1 - self.BULK_DISCOUNT)
        return price


# Example test case
def run_tests():
    # Create e-books for the catalog
    ebook1 = Ebook("Good Doctor", "Amber Ali", "2022-012-01", "Education", 38.00)
    ebook2 = Ebook("Math and Simson", "Khalil Abdu", "2022-11-15", "Education", 30.00)
    ebook3 = Ebook("Cyber Security", "Stephan Moull", "2021-10-10", "Programming", 35.00)
    ebook4 = Ebook("Open The Soul", "Mickel Ali", "2021-04-19", "Horror", 40.00)
    ebook5 = Ebook("Sound Of The Police", "Nardin Harris", "2019-06-21", "Comedy", 50.00)

    print("E-book Catalog:")
    for ebook in [ebook1, ebook2, ebook3, ebook4, ebook5]:
        print(ebook)

    # Test case for a customer with loyalty membership and bulk purchase (5 books)
    print("\nTest Case 1: Loyalty Member with Bulk Purchase")
    customer1 = Customer("Mahra", "Mahra@gmail.com", is_loyalty_member=True)
    cart1 = ShoppingCart(customer1)
    cart1.add_item(ebook1)
    cart1.add_item(ebook2)
    cart1.add_item(ebook3)
    cart1.add_item(ebook4)
    cart1.add_item(ebook5)

    order1 = Order(cart1)
    invoice1 = order1.generate_invoice()
    print(order1)
    print(invoice1)

    # Test case for a customer without loyalty membership and bulk purchase (5 books)
    print("\nTest Case 2: No Loyalty Member with Bulk Purchase")
    customer2 = Customer("Mohamed", "Mohamed@gmail.com", is_loyalty_member=False)
    cart2 = ShoppingCart(customer2)
    cart2.add_item(ebook1)
    cart2.add_item(ebook2)
    cart2.add_item(ebook3)
    cart2.add_item(ebook4)
    cart2.add_item(ebook5)

    order2 = Order(cart2)
    invoice2 = order2.generate_invoice()
    print(order2)
    print(invoice2)

    # Test case for a customer with loyalty membership and small purchase (2 books)
    print("\nTest Case 3: Loyalty Member with Small Purchase")
    customer3 = Customer("Khaled Eisse", "khaled@gmail.com", is_loyalty_member=True)
    cart3 = ShoppingCart(customer3)
    cart3.add_item(ebook1)
    cart3.add_item(ebook2)

    order3 = Order(cart3)
    invoice3 = order3.generate_invoice()
    print(order3)
    print(invoice3)

    # Test case for a customer without loyalty membership and small purchase (2 books)
    print("\nTest Case 4: No Loyalty Member with Small Purchase")
    customer4 = Customer("Ismaiel Mohamed", "Ismail@gmail.com", is_loyalty_member=False)
    cart4 = ShoppingCart(customer4)
    cart4.add_item(ebook1)
    cart4.add_item(ebook2)

    order4 = Order(cart4)
    invoice4 = order4.generate_invoice()
    print(order4)
    print(invoice4)


# Run the test case
run_tests()
