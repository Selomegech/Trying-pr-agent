import datetime

class Product:
    """Represents a product in the catalog."""
    def __init__(self, product_id, name, price, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category

class OrderManager: # CODE SMELL: Large Class - Manages products, orders, promotions, and processing.
    """
    Manages products, processes orders, applies promotions, and handles logging.
    Violates Single Responsibility Principle.
    """

    def __init__(self):
        self.products = {} # Stores product_id -> Product object
        self.active_promotions = [] # Stores active promotion codes
        self.order_history = []
        self._load_initial_data()

    def _load_initial_data(self):
        """Simulates loading some initial product data."""
        self.add_product(Product(101, "Laptop", 1200.00, "Electronics"))
        self.add_product(Product(102, "Mouse", 25.00, "Electronics"))
        self.add_product(Product(201, "Keyboard", 75.00, "Electronics"))
        self.add_product(Product(301, "Coffee Mug", 12.50, "Home Goods"))
        self.add_promotion("FREESHIP")
        self.add_promotion("SAVE10")

    def add_product(self, product: Product):
        if product.product_id not in self.products:
            self.products[product.product_id] = product
            print(f"Added product: {product.name}")
        else:
            print(f"Product ID {product.product_id} already exists.")

    def add_promotion(self, code: str):
        if code not in self.active_promotions:
            self.active_promotions.append(code)
            print(f"Added promotion: {code}")
        else:
            print(f"Promotion code {code} already active.")

    def process_customer_order(self, order_id, customer_info, items_list, shipping_address, promotion_code=None): # CODE SMELL: Long Method, Long Parameter List
        """
        Processes a customer's order from start to finish.
        This single method handles validation, price calculation, promotion application,
        shipping cost, and order finalization.
        """
        print(f"\n--- Processing Order {order_id} ---")
        order_date = datetime.datetime.now()
        total_price = 0.0
        shipping_cost = 0.0
        discount_amount = 0.0
        final_status = "Pending"
        
        # CODE SMELL: Deep Nesting for initial validation
        if not items_list:
            print("ERROR: Order must contain items.")
            return {"status": "Failed", "reason": "No items"}
        if not customer_info or not customer_info.get('email'):
            print("ERROR: Customer email is required.")
            return {"status": "Failed", "reason": "Missing customer info"}
        
        # Calculate item prices
        for item in items_list:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            
            # CODE SMELL: Duplicate Code (product lookup)
            if product_id in self.products:
                product = self.products[product_id]
                item_total = product.price * quantity
                total_price += item_total
                print(f"Item: {product.name}, Quantity: {quantity}, Price: ${item_total:.2f}")
            else:
                print(f"WARNING: Product ID {product_id} not found. Skipping item.")
                final_status = "Failed (Product Not Found)"
                
        # Apply promotions
        if promotion_code and promotion_code in self.active_promotions:
            if promotion_code == "FREESHIP": # CODE SMELL: Magic String
                shipping_cost = 0.0
                discount_amount += 10.0 # Simulate average shipping cost saving
                print("Applied FREESHIP promotion.")
            elif promotion_code == "SAVE10": # CODE SMELL: Magic String
                discount_amount += total_price * 0.10 # CODE SMELL: Magic Number (0.10)
                total_price -= discount_amount # Apply discount to total
                print("Applied SAVE10 promotion.")
            else:
                print(f"Unknown active promotion code: {promotion_code}")
        elif promotion_code:
            print(f"Promotion code '{promotion_code}' is invalid or expired.")
            
        # Determine shipping cost based on location
        if "US" in shipping_address: # CODE SMELL: Magic String
            if total_price < 50.0: # CODE SMELL: Magic Number
                shipping_cost = 5.00 # CODE SMELL: Magic Number
            else:
                shipping_cost = 7.50 # CODE SMELL: Magic Number
        else: # International shipping
            shipping_cost = 25.00 # CODE SMELL: Magic Number
            
        # Final calculations
        final_price = total_price + shipping_cost - discount_amount
        
        order_details = {
            "order_id": order_id,
            "customer_email": customer_info.get('email'),
            "items": items_list,
            "subtotal": total_price + discount_amount, # Recalculate original subtotal
            "discount_applied": discount_amount,
            "shipping_cost": shipping_cost,
            "final_amount": max(0, final_price), # Ensure final amount isn't negative
            "order_date": order_date.isoformat(),
            "status": final_status
        }
        
        self.order_history.append(order_details)
        print(f"Order {order_id} processed. Final Amount: ${order_details['final_amount']:.2f}")
        return order_details

    def get_order_summary(self, order_id):
        """Retrieves and prints a summary for a given order ID."""
        for order in self.order_history:
            if order.get('order_id') == order_id:
                print(f"\n--- Order Summary for {order_id} ---")
                print(f"Status: {order['status']}")
                print(f"Date: {order['order_date']}")
                print(f"Customer: {order['customer_email']}")
                print(f"Subtotal: ${order['subtotal']:.2f}")
                print(f"Discount: ${order['discount_applied']:.2f}")
                print(f"Shipping: ${order['shipping_cost']:.2f}")
                print(f"Final Amount: ${order['final_amount']:.2f}")
                return
        print(f"Order {order_id} not found in history.")


if __name__ == '__main__':
    manager = OrderManager()

    customer1_info = {"name": "Alice Smith", "email": "alice@example.com"}
    customer2_info = {"name": "Bob Johnson", "email": "bob@example.com"}

    # Order 1: Standard order with discount
    items_a = [
        {'product_id': 101, 'quantity': 1},
        {'product_id': 102, 'quantity': 2}
    ]
    order_a = manager.process_customer_order(1, customer1_info, items_a, "123 Main St, Anytown, US", "SAVE10")
    
    # Order 2: Free shipping, some items not found
    items_b = [
        {'product_id': 201, 'quantity': 1},
        {'product_id': 999, 'quantity': 1} # Non-existent product
    ]
    order_b = manager.process_customer_order(2, customer2_info, items_b, "456 Ocean Ave, Metropolis, US", "FREESHIP")

    # Order 3: International shipping, no promotion
    items_c = [
        {'product_id': 301, 'quantity': 3}
    ]
    order_c = manager.process_customer_order(3, customer1_info, items_c, "789 High St, London, UK")

    manager.get_order_summary(1)
    manager.get_order_summary(2)
    manager.get_order_summary(3)
    manager.get_order_summary(4) # Non-existent order summary