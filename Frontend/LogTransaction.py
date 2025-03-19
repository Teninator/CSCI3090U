import os

"""
LogTransaction.py
Handles writing transactions to a log file.
"""

class LogTransactionFile:
    def __init__(self):
        self.transaction_code = '00'
        self.account_holder_name = 20 * '_'
        self.account_number = 5 * '0'
        self.amount = '00000.00'
        self.misc = '__'
        self.transaction_line = ''

    def format_account_holder_name(self):
        """Formats the account holder's name to be 20 characters long with underscores."""
        formatted_name = self.account_holder_name.replace(' ', '_').ljust(20, '_')
        return formatted_name

    def format_account_number(self):
        """Ensures the account number is always 5 digits, padding with zeros if necessary."""
        return self.account_number.zfill(5)

    def format_amount(self):
        """Formats the amount as a zero-padded 5-digit value with '.00' appended."""
        amount_str = str(int(float(self.amount)))  # Ensure it's an integer before formatting
        return amount_str.zfill(5) + ".00"

    def create_transaction_line(self):
        """Creates the formatted transaction line by concatenating all required fields."""
        formatted_name = self.format_account_holder_name()
        formatted_acc_num = self.format_account_number()
        formatted_amount = self.format_amount()
        self.transaction_line = f"{self.transaction_code}_{formatted_name}_{formatted_acc_num}_{formatted_amount}_{self.misc}"

    def write_transaction_to_file(self, filename):
        """Appends the formatted transaction line to the specified file."""
        with open(filename, "a") as file:
            file.write(self.transaction_line + "\n")

    def prepare_write(self, transaction_code='00',
                      account_holder_name=20 * '_',
                      account_number=5 * '0',
                      amount='00000.00',
                      misc='__'):
        """Prepares the transaction line to be written by calling all the necessary formatting functions."""
        self.transaction_code = transaction_code
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.amount = amount
        self.misc = misc
        self.create_transaction_line()
