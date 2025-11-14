import json
import datetime

class Product:
    """
    A base class for all products.
    """
    def __init__(self, item_id, name, price, stock_level):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.stock_level = stock_level
        self.is_active = True
        
    def calculate_taxable_price(self):
        """
        Base tax calculation for standard items (10% tax rate).
        """
        return self.price * 1.10

class BookProduct(Product):
    """
    A specific product type: Books.
    """
    def __init__(self, item_id, name, price, stock_level, author, isbn):
        super().__init__(item_id, name, price, stock_level)
        self.author = author
        self.isbn = isbn

class SoftwareProduct(Product):
    """
    A specific product type: Software licenses.
    CODE SMELL: Refused Bequest (Tax rate is completely different and hardcoded).
    """
    def __init__(self, item_id, name, price, stock_level, license_key_count, platform):
        super().__init__(item_id, name, price, stock_level)
        self.license_key_count = license_key_count
        self.platform = platform

    def calculate_taxable_price(self):
        """
        Overrides parent method completely because software has a special 5% tax.
        The system should ideally use a Strategy pattern for taxes, not inheritance.
        """
        print(f"Applying special software tax for {self.name}...")
        return self.price * 1.05


class InventoryMasterSystem:
    """
    CODE SMELL: Large Class (God Object). This class handles all data management, 
    validation, and reporting logic, violating the Single Responsibility Principle (SRP).
    """
    def __init__(self, initial_products):
        self.inventory_data = {}
        for product in initial_products:
            self.inventory_data[product.item_id] = product
        self.audit_log = []
        self.today = datetime.date.today().strftime("%Y-%m-%d")

    def log_activity(self, activity):
        # CODE SMELL: Utility logic mixed in with core business logic.
        self.audit_log.append(f"[{self.today}] {activity}")

    def process_product_data_and_validate(self, new_product_list, threshold=50, max_price=1000.0):
        """
        CODE SMELL: Long Method. This single method handles data parsing, validation, 
        stock updating, and reporting/logging—it does too many things.
        """
        self.log_activity("Starting batch data processing and validation.")

        # --- 1. Data Parsing and Preparation ---
        parsed_count = 0
        for data in new_product_list:
            
            # CODE SMELL: Validation logic mixed with processing
            if not isinstance(data.get('id'), int) or data.get('id') <= 0:
                self.log_activity(f"ERROR: Invalid ID detected in data: {data}")
                continue # Skip invalid records

            item_id = data['id']
            new_stock = data.get('stock', 0)
            
            # --- 2. Input Validation (Complex Logic) ---
            if new_stock < 0:
                # CODE SMELL: Comment as Crutch. Explaining bad logic instead of fixing it.
                # We should really raise an exception here, but for now we just fix the stock to 0.
                new_stock = 0
                self.log_activity(f"WARNING: Negative stock corrected for Item {item_id}.")
            
            # --- 3. Business Logic and Stock Update ---
            if item_id in self.inventory_data:
                product = self.inventory_data[item_id]
                old_stock = product.stock_level
                product.stock_level = new_stock
                self.log_activity(f"Stock updated for {product.name}: {old_stock} -> {new_stock}")
                parsed_count += 1
            else:
                self.log_activity(f"ALERT: Item ID {item_id} not found. Skipping update.")
                continue 

            # --- 4. Reporting/Alert Generation (Another responsibility) ---
            if new_stock < threshold: # CODE SMELL: Magic Number (threshold) used in parameter
                self.log_activity(f"CRITICAL: {product.name} ({item_id}) stock is low ({new_stock}). Reorder required.")
            
            # --- 5. Price Check and Flagging ---
            if product.price > max_price:
                product.is_active = False # Temporarily deactivates product if price is too high
                self.log_activity(f"INFO: {product.name} deactivated due to high price ({product.price}).")

        self.log_activity(f"Finished processing {parsed_count} product records.")
        return parsed_count

    def generate_stock_report(self):
        """
        Generates a summary of all inventory, including taxable price.
        """
        report = {"total_items": len(self.inventory_data), "report_date": self.today, "details": []}
        
        for item_id, product in self.inventory_data.items():
            report['details'].append({
                "id": item_id,
                "name": product.name,
                "stock": product.stock_level,
                "taxed_price": f"${product.calculate_taxable_price():.2f}"
            })
            
        return json.dumps(report, indent=4)


if __name__ == '__main__':
    # Initial setup with diverse product types
    book_a = BookProduct(101, "The Pragmatic Programmer", 45.00, 75, "Andrew Hunt", "978-0135957059")
    software_x = SoftwareProduct(205, "ProDev IDE License", 999.00, 20, 500, "Windows/Mac")

    manager = InventoryMasterSystem(initial_products=[book_a, software_x])
    
    # Data to be processed (new batch updates)
    new_data = [
        {'id': 101, 'stock': 20}, # Low stock
        {'id': 205, 'stock': -5}, # Negative stock corrected
        {'id': 300, 'stock': 100}, # New ID (skipped)
    ]
    
    # Run the long method
    records_processed = manager.process_product_data_and_validate(new_data, threshold=30, max_price=500.0)

    print(f"\nProcessed {records_processed} records.")
    
    # Generate report
    print("\n" + manager.generate_stock_report())
    
    # Audit trail
    print("\n--- Audit Log ---")
    for log in manager.audit_log:
        print(log)