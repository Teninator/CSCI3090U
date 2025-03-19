"""
bank-atm.py
Main application file that integrates all components to process transactions.
Run using below syntax where :
param 1 is the path to the bank account file
param 2 is the path to the transaction log file
python bank-atm.py CurrentBankAccounts.txt transout.atf
"""

import sys
from BankData import BankData
from LogTransaction import LogTransactionFile
from Transaction import Transaction

def main():
    """
    Main function that initializes components and processes transactions from user input.
    """

    # Ensure correct number of arguments
    if len(sys.argv) < 3:
        print("Usage: python bank-atm.py <accounts_file> <transaction_file>")
        sys.exit(1)

    accounts_file = sys.argv[1]  # First argument: accounts file
    transaction_file = sys.argv[2]  # Second argument: transaction log file
    logged_in = False
    ts = Transaction(accounts_file, transaction_file)
    
    while not logged_in:
        num_transactions = 0
        print("Welcome to the Banking System.")
         
        user_input = str.lower(input())
        
        # Exit command
        if user_input == "exit":
            ts.log_transaction_file_end()
            break
        
        # First transaction must be login
        res = ts.process_transaction(user_input)
        
        # After login, process multiple transactions
        while res:
            logged_in = True
            print("Please enter your transaction: ")
            user_input = str.lower(input())
            
            # Exit command
            if user_input == "exit":
                ts.log_transaction_file_end()
                break
            
            res = ts.process_transaction(user_input)
            if res:
                num_transactions += 1
                print("Transaction Successful.")
            else:
                ts.log_transaction_file_end()
                ts = Transaction(accounts_file, transaction_file)  # Reset session
                print("Session terminated.")
        

if __name__ == "__main__":
    main()

