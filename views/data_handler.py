import csv
import os

class DataHandler:
    def __init__(self):
        self.data_directory = "data"

    def load_data(self):
        businesses = {}
        if os.path.exists(self.data_directory):
            for filename in os.listdir(self.data_directory):
                if filename.endswith(".csv"):
                    business_name = filename[:-4]
                    businesses[business_name] = {
                        "type": None,
                        "transactions": [],
                        "chart_of_accounts": self.predefined_chart_of_accounts()
                    }
                    with open(os.path.join(self.data_directory, filename), newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            businesses[business_name]["transactions"].append(row)
        return businesses

    def save_data(self, businesses):
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        for business_name, business_data in businesses.items():
            with open(os.path.join(self.data_directory, f"{business_name}.csv"), mode='w', newline='') as csvfile:
                fieldnames = ["date", "amount", "debit_account", "credit_account", "description"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for transaction in business_data["transactions"]:
                    writer.writerow(transaction)

    def predefined_chart_of_accounts(self):
        return {
            "Assets": {
                "1000 Cash on Hand": "Cash on Hand",
                "1010 Cash in Bank": "Cash in Bank",
                "1020 Petty Cash": "Petty Cash",
                "1100 Accounts Receivable": "Accounts Receivable",
                "1200 Inventory - Cars": "Inventory - Cars",
                "1210 Inventory - Parts and Accessories": "Inventory - Parts and Accessories",
                "1300 Prepaid Expenses": "Prepaid Expenses",
                "1500 Land": "Land",
                "1510 Buildings": "Buildings",
                "1520 Leasehold Improvements": "Leasehold Improvements",
                "1530 Office Equipment": "Office Equipment",
                "1540 Computer Equipment": "Computer Equipment",
                "1550 Furniture and Fixtures": "Furniture and Fixtures",
                "1560 Vehicles": "Vehicles",
                "1570 Accumulated Depreciation": "Accumulated Depreciation"
            },
            "Liabilities": {
                "2000 Accounts Payable": "Accounts Payable",
                "2100 Short-term Loans": "Short-term Loans",
                "2200 Sales Tax Payable": "Sales Tax Payable",
                "2300 Payroll Liabilities": "Payroll Liabilities",
                "2400 Unearned Revenue": "Unearned Revenue",
                "2500 Customer Deposits": "Customer Deposits",
                "2600 Long-term Loans": "Long-term Loans",
                "2700 Mortgage Payable": "Mortgage Payable"
            },
            "Equity": {
                "3000 Owner’s Equity": "Owner’s Equity",
                "3010 Owner’s Capital": "Owner’s Capital",
                "3020 Owner’s Drawings": "Owner’s Drawings",
                "3100 Retained Earnings": "Retained Earnings"
            },
            "Revenue": {
                "4000 Sales Revenue": "Sales Revenue",
                "4010 Car Sales Revenue": "Car Sales Revenue",
                "4020 Parts and Accessories Sales": "Parts and Accessories Sales",
                "4030 Service Revenue": "Service Revenue",
                "4040 Extended Warranty Revenue": "Extended Warranty Revenue",
                "4050 Financing Revenue": "Financing Revenue",
                "4100 Advertising Revenue": "Advertising Revenue",
                "4200 Interest Income": "Interest Income"
            },
            "Cost of Goods Sold (COGS)": {
                "5000 Cost of Goods Sold": "Cost of Goods Sold",
                "5010 Cost of Cars Sold": "Cost of Cars Sold",
                "5020 Cost of Parts and Accessories Sold": "Cost of Parts and Accessories Sold",
                "5030 Cost of Services": "Cost of Services"
            },
            "Operating Expenses": {
                "6000 Selling Expenses": "Selling Expenses",
                "6010 Advertising and Promotion": "Advertising and Promotion",
                "6020 Sales Commissions": "Sales Commissions",
                "6030 Website Maintenance": "Website Maintenance",
                "6040 Marketing Expenses": "Marketing Expenses",
                "6100 Administrative Expenses": "Administrative Expenses",
                "6110 Office Supplies": "Office Supplies",
                "6120 Rent Expense": "Rent Expense",
                "6130 Utilities Expense": "Utilities Expense",
                "6140 Insurance Expense": "Insurance Expense",
                "6150 Depreciation Expense": "Depreciation Expense",
                "6160 Salaries and Wages": "Salaries and Wages",
                "6170 Payroll Taxes": "Payroll Taxes",
                "6180 Professional Fees": "Professional Fees",
                "6200 Other Operating Expenses": "Other Operating Expenses",
                "6210 Vehicle Maintenance": "Vehicle Maintenance",
                "6220 Fuel and Oil": "Fuel and Oil",
                "6230 Licensing and Registration": "Licensing and Registration",
                "6240 Training and Development": "Training and Development",
                "6250 Bank Charges": "Bank Charges",
                "6260 Travel and Entertainment": "Travel and Entertainment"
            },
            "Non-Operating Expenses": {
                "7000 Interest Expense": "Interest Expense",
                "7100 Loss on Sale of Assets": "Loss on Sale of Assets"
            }
        }
