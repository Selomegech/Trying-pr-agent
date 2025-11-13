import datetime

class CustomerAccount:
    """
    Represents a customer's account details and billing information.
    """
    def __init__(self, account_id, name, monthly_rate_usd, services_used):
        # Primitive Obsession: Uses basic types instead of custom objects
        self.account_id = account_id
        self.name = name
        self.monthly_rate = monthly_rate_usd # CODE SMELL: Magic Number potential
        self.services_used = services_used # list of strings/objects
        self.last_payment_date = datetime.date.today() - datetime.timedelta(days=35)


class BillingReportGenerator:
    """
    Generates a detailed monthly billing report.
    This class is too tightly coupled to the internal structure of CustomerAccount.
    """
    def __init__(self, tax_rate_percent=8.5): 
        self.TAX_RATE = tax_rate_percent / 100.0
        self.REPORT_DATE = datetime.date.today()

    def generate_detailed_bill(self, account: CustomerAccount):
        """
        Calculates charges and generates a detailed invoice breakdown.
        """
        
        
        
        # Calculate base charge
        base_charge = account.monthly_rate
        
        # Calculate usage-based fees (CODE SMELL: Hardcoded fee)
        usage_fee = len(account.services_used) * 15.50
        
        # Check for late payment
        days_late = (self.REPORT_DATE - account.last_payment_date).days
        late_fee = 0
        if days_late > 30: # CODE SMELL: Magic Number (30)
            late_fee = base_charge * 0.10 # CODE SMELL: Magic Number (0.10) for 10% late fee
            
        subtotal = base_charge + usage_fee + late_fee
        tax_amount = subtotal * self.TAX_RATE
        total_due = subtotal + tax_amount
        
        # Report generation (CODE SMELL: Long string/Complex formatting)
        report = (
            f"*** Monthly Invoice for {account.name} (ID: {account.account_id}) ***\n"
            f"Billing Period: {self.REPORT_DATE.strftime('%Y-%m')}\n"
            f"----------------------------------------------------\n"
            f"Base Monthly Rate: ${base_charge:.2f}\n"
            f"Usage Fee ({len(account.services_used)} services): ${usage_fee:.2f}\n"
            f"Late Fee (Days Late: {days_late}): ${late_fee:.2f}\n"
            f"Subtotal: ${subtotal:.2f}\n"
            f"Tax ({self.TAX_RATE * 100:.1f}%): ${tax_amount:.2f}\n"
            f"----------------------------------------------------\n"
            f"TOTAL DUE: ${total_due:.2f}\n"
            f"Last Payment: {account.last_payment_date}\n"
        )
        return report

    def summarize_billing_cycle(self, accounts_list, start_date, end_date, currency="USD"): # CODE SMELL: Long Parameter List
        """
        A summary function that could be broken down into smaller pieces.
        """
        
        total_billing = 0
        for acc in accounts_list:
            # Re-calculating logic that should potentially be cached or part of the CustomerAccount
            base_charge = acc.monthly_rate
            usage_fee = len(acc.services_used) * 15.50
            late_fee = 0
            
            # Simplified late fee check for summary
            if (self.REPORT_DATE - acc.last_payment_date).days > 30:
                late_fee = base_charge * 0.10
                
            subtotal = base_charge + usage_fee + late_fee
            total_billing += subtotal
            
        summary = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "currency": currency,
            "total_accounts": len(accounts_list),
            "total_gross_billing": total_billing
        }
        return summary


if __name__ == '__main__':
    # Setup
    customer_a = CustomerAccount(1001, "Acme Corp", 99.99, ["API", "Storage", "Analytics"])
    customer_b = CustomerAccount(1002, "Beta Ltd", 49.99, ["API"])
    customer_b.last_payment_date = datetime.date.today() - datetime.timedelta(days=45) # Make this one late

    generator = BillingReportGenerator(tax_rate_percent=7.0)
    
    # Run detailed bill
    bill_a = generator.generate_detailed_bill(customer_a)
    print("--- CUSTOMER A BILL ---")
    print(bill_a)

    bill_b = generator.generate_detailed_bill(customer_b)
    print("--- CUSTOMER B BILL (LATE) ---")
    print(bill_b)

    # Run summary
    all_accounts = [customer_a, customer_b]
    summary = generator.summarize_billing_cycle(
        all_accounts, 
        datetime.date.today() - datetime.timedelta(days=30), 
        datetime.date.today(), 
        currency="USD"
    )
    print("--- MONTHLY SUMMARY ---")
    print(summary)