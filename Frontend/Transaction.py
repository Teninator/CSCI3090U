from BankData import BankData
from LogTransaction import LogTransactionFile
from datetime import datetime
import os

"""
Transaction.py
Handles transaction processing by validating inputs, interacting with BankData,
and logging transactions using LogTransaction.
"""


class Transaction:
    def __init__(self, accounts_file = "", transaction_file = ""):
        """
        Initializes the Transaction class with bank data and log file.

        :param bank_data: Instance of BankData for account validation.
        :param log_file: Instance of LogTransaction for logging transactions.
        """
        self.bank_data = BankData(dir = accounts_file)
        self.log_file = LogTransactionFile()
        self.session_type = ""
        self.account_number = 0
        self.username = ""
        self.amount = 0
        current_time = datetime.now().strftime("%H:%M").replace(":", "_")
        self.transaction_file = transaction_file
        self.isLogged = False
        

    def verify_account(self, username, account_number):
        """
        Verify if the account exists and matches the given username.
        :return: True if valid, False otherwise.
        """
        if not self.bank_data.validate_acc_num(account_number):
            return False
        return self.bank_data.validate_user_and_account_num_match(username, account_number)


    def process_transaction(self, transaction_type, amount=0, target_account=None):
        """
        Handle all transactions by validating it and updating bank data.

        :param transaction_type: Transaction details as a string.
        :return: True if transaction is successful, False otherwise.
        """
        if transaction_type == "login":
            if not self.isLogged:
                print("Please enter the session type(standard/admin): ")
                self.session_type = str.lower(input())

                if self.session_type == "standard":
                    print("Please enter the account holder's name: ")
                    self.username = input()

                    if self.bank_data.validate_name(self.username):
                        print("You are now in standard user mode.")
                        self.isLogged = True
                        return True
                    
                    else:
                        print("Transaction rejected. Reason: Account holder name is invalid.")
                if self.session_type == "admin":
                    print("You are now in admin user mode.")
                    self.isLogged = True
                    return True
            else:
                print("Transaction rejected. Reason: invalid transaction.")
                return False
            return False
        
        if not self.isLogged:
            print("Transaction rejected. Reason: No transaction before login.")
            return False

        if transaction_type == "withdrawal":
            if self.session_type == "admin":
                print("Please enter the account holder's name: ")
                self.username = input()
                
            if self.bank_data.validate_name(self.username):
                print("Please enter the account number: ")
                self.account_number = input()
                if self.verify_account(self.username, self.account_number):
                    print("Please enter the amount to withdraw: ")
                    temp_amount = input()
                    if temp_amount.isdigit():
                        temp_amount = int(temp_amount)
                        if temp_amount < 0:
                            print("Transaction rejected. Reason: Invalid amount to withdraw.")
                            return False
                        self.amount = temp_amount
                    else:
                        print("Transaction rejected. Reason: Invalid amount to withdraw.")
                        return False

                    if self.session_type =="standard" and\
                        self.amount > 500:
                            print("Transaction rejected. Reason: the maximum allowed amount is $500.00.")
                            return False
                    elif self.bank_data.validate_balance(self.account_number, self.amount):
                        self.log_file.prepare_write("01", self.username, self.account_number, self.amount)
                        self.log_file.write_transaction_to_file(filename=self.transaction_file)
                        return True
                    else:
                        print("Transaction rejected. Reason: Insufficient funds.")
                        return False
                else:
                    print("Transaction rejected. Reason: Account number is invalid.")
            else:
                print("Transaction rejected. Reason: Account holder name is invalid.")
                return False
                
            return False
        
        elif transaction_type == "transfer":
            if self.session_type == "admin":
                print("Please enter the account holder's name: ")
                self.username = input()
                
            if self.bank_data.validate_name(self.username):
                print("Please enter the account number to transfer from: ")
                self.account_number = input()
                if self.verify_account(self.username, self.account_number):
                    print("Please enter the account number to transfer to: ")
                    receiver_account_number = input()
                    if(self.account_number == receiver_account_number):
                        print("Transaction rejected. Reason: Account number is invalid.")
                        return False
                    if(self.bank_data.validate_acc_num(receiver_account_number)):
                        print("Please enter the amount to transfer: ")
                        temp_amount = input()
                        if temp_amount.isdigit():
                            temp_amount = int(temp_amount)
                            if temp_amount < 0:
                                print("Transaction rejected. Reason: Invalid amount to withdraw.")
                                return False
                            self.amount = temp_amount
                        else:
                            print("Transaction rejected. Reason: Invalid amount to withdraw.")
                            return False
                        
                    else:
                        print("Transaction rejected. Reason: Account number is invalid.")
                        return False
                    
                    if self.session_type =="standard" and\
                        self.amount > 1000:
                            print("Transaction rejected. Reason: the maximum allowed amount is $1000.00.")
                            return False
                    elif self.bank_data.validate_balance(self.account_number, self.amount) and\
                        self.bank_data.validate_balance(receiver_account_number, self.amount, is_receiving=True):
                            
                        print(f"Transferred ${float(self.amount):.2f} from {self.account_number} to {receiver_account_number}.")
                        
                        self.log_file.prepare_write("02", self.username, self.account_number, self.amount)
                        self.log_file.write_transaction_to_file(filename= self.transaction_file)

                        self.log_file.prepare_write("02", self.bank_data.get_name_by_acc_num(receiver_account_number),
                         receiver_account_number, self.amount)
                        self.log_file.write_transaction_to_file(filename= self.transaction_file)
                        return True
                    else:
                        print("Transaction rejected. Reason: Insufficient funds.")
                        return False
                else:
                    print("Transaction rejected. Reason: Account number is invalid.")    
            else:
                print("Transaction rejected. Reason: Account holder name is invalid.")
                return False
            
            return False

        elif transaction_type == "paybill":
            if self.session_type == "admin":
                print("Please enter the account holder's name: ")
                self.username = input()
                
            if self.bank_data.validate_name(self.username):
                print("Please enter the account number: ")
                self.account_number = input()
                if self.verify_account(self.username, self.account_number):
                    print("Please enter the company name for bill payment: ")
                    company_name = input()
                    if(company_name in ["EC", "CQ", "FI", "The Bright Light Electric Company", "Credit Card Company Q", "Fast Internet, Inc."]):
                        try:
                            print("Please enter the amount to transfer: ")
                            self.amount = int(input())
                        except ValueError:
                            print("Transaction rejected. Reason: invalid amount.")
                            return False

                        if (self.session_type =="standard" and self.amount > 2000) or self.amount < 0 :
                            print("Transaction rejected. Reason: invalid amount.")
                            return False
                        elif self.bank_data.validate_balance(self.account_number, self.amount):
                            mapping = {
                                "The Bright Light Electric Company": "EC",
                                "Credit Card Company Q": "CQ",
                                "Fast Internet, Inc.": "FI"
                            }
                            company_name = mapping.get(company_name, company_name)
                            print(f"Transferred ${float(self.amount):.2f} to {company_name}.")
                            self.log_file.prepare_write("03", self.username, self.account_number, self.amount, company_name)
                            self.log_file.write_transaction_to_file(filename= self.transaction_file)
                            return True
                        else:
                            print("Transaction rejected. Reason: invalid amount.")
                    else:
                        print("Transaction rejected. Reason: invalid company name.")
                else:
                    print("Transaction rejected. Reason: invalid account number.")
            else:
                print("Transaction rejected. Reason: invalid account holder name.")
                
            return False
        
        elif transaction_type == "deposit":
            if self.session_type == "admin":
                print("Please enter the account holder's name: ")
                self.username = input()
                
            if self.bank_data.validate_name(self.username):
                print("Please enter the account number: ")
                self.account_number = input()
                if self.verify_account(self.username, self.account_number):
                    try:
                        print("Please enter the amount to deposit: ")
                        self.amount = int(input())
                    except ValueError:
                        print("Transaction rejected. Reason: invalid amount.")
                        return False

                    if self.amount > 0 and self.bank_data.validate_balance(self.account_number, self.amount, is_receiving=True):
                        print(f"Deposited ${float(self.amount):.2f} in account: {self.account_number}.")
                        self.log_file.prepare_write("04", self.username, self.account_number, self.amount)
                        self.log_file.write_transaction_to_file(filename= self.transaction_file)
                        return True
                    else:
                        print("Transaction rejected. Reason: invalid amount.")
                else:
                    print("Transaction rejected. Reason: invalid account number.")
            else:
                print("Transaction rejected. Reason: invalid account holder name.")
            
            return False
        
        elif transaction_type == "create":
            if self.session_type == "admin":
                print("Please enter the account holder's name: ")
                self.username = input()
                if(len(self.username) <= 20 and self.username.replace(" ", "").isalpha()):
                    
                    print("Please enter the initial balance of the account: ")
                    user_input = input().strip().lower()
                    if (user_input == "logout"):
                        return False
                    try:   
                        self.amount = int(user_input)

                  
                        if (self.amount < 99999 and self.amount>0):
                            self.log_file.prepare_write("05", self.username, "", self.amount)
                            self.log_file.write_transaction_to_file(filename= self.transaction_file)
                            return True
                        else:
                            print("Transaction rejected. Reason: initial balance should be between 0 and 99999.99.")
                            return False
                    except ValueError:
                        print("Transaction rejected. Reason: initial balance should be between 0 and 99999.99.")
                        

                else:
                    print("Invalid account holder name. Reason: Name exceeds 20 characters.")
                    
            else:
                print("Transaction rejected. Reason: You need to be in admin mode.")
                
            
            return False
        
        elif transaction_type == "delete":
            if self.session_type == "admin":
                print("Please enter the account holder's name: ")
                self.username = input()
                if self.bank_data.validate_name(self.username):
                    print("Please enter the account number: ")
                    acc_num_input = input().strip().lower()
                    if (acc_num_input == "logout"):
                        return False
                    
                    self.account_number = acc_num_input
                    if self.verify_account(self.username, self.account_number):  
                        self.log_file.prepare_write("06", self.username, self.account_number)
                        self.log_file.write_transaction_to_file(filename= self.transaction_file)
                        return True
                    else:
                        print("Transaction rejected. Reason: account number should be an existing number.")
                        return False
                elif self.username == "logout":
                    return False
                else:
                    print("Transaction rejected. Reason: Account holder must be an existing one.")
                    return False
            else:
                print("Transaction rejected. Reason: You need to be in admin mode.")
                
            
            return False
        
        elif transaction_type == "disable":
            if self.session_type == "admin":
                print("Please enter the account holder's name: ")
                self.username = input()
                if (self.username == "logout"):
                    return False
                if self.bank_data.validate_name(self.username):
                    print("Please enter the account number: ")
                    self.account_number = input()
                    if (self.account_number == "logout"):
                        return False
                    if self.verify_account(self.username, self.account_number):
                        self.log_file.prepare_write("07", self.username, self.account_number)
                        self.log_file.write_transaction_to_file(filename= self.transaction_file)
                        return True
                    else:
                        print("Transaction rejected. Reason: Account number must be an existing number")
                        
                else:
                    print("Transaction rejected. Reason: Account holder must be an existing one.")
                    
            else:
                print("Transaction rejected. Reason: You need to be in admin mode.")
                return False
                
            return False
        
        elif transaction_type == "changeplan":
            if self.session_type == "admin":
                print("Please enter the account holder's name: ")
                self.username = input()
                if self.bank_data.validate_name(self.username):
                    print("Please enter the account number: ")
                    self.account_number = input()
                    if self.verify_account(self.username, self.account_number):
                        self.log_file.prepare_write("08", self.username, self.account_number, misc="SP")
                        self.log_file.write_transaction_to_file(filename= self.transaction_file)
                        return True
                    
                    else:
                        print("Transaction rejected. Reason: Account number is invalid")
                        
                else:
                    print("Transaction rejected. Reason: Account holder is invalid")
                    
            else:
                print("Transaction rejected. Reason: You need to be in admin mode.")
                
            
            return False
        
        elif transaction_type == "logout":
            return False
        
        else:
            print("Transaction rejected. Reason: invalid transaction.")
            return False

    def log_transaction_file_end(self):
        self.log_file.prepare_write()
        self.log_file.write_transaction_to_file(filename = self.transaction_file)
    


        


     
        


