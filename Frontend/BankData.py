"""
BankData.py
Handles the management of bank accounts, including loading, retrieving, and updating account balances.
"""

class BankData:
    def __init__(self, dir):
        """
        Initializes the BankData class and loads account details from a file.
        
        :param dir: The file containing bank account information.
        """
        self.dir = dir
        self.data = []
        self.read_data()  # Populates self.data

    def read_data(self):
        with open(self.dir, "r") as f:
            for line in f:
                entry = {
                    "Acc_Num": line[:5].lstrip("0"),
                    "Name": line[5:27].strip('_').replace("_", " "),
                    "Status": line[27:28],
                    "Balance": float(line[29:].strip())
                }
                self.data.append(entry)

    # GETTERS ------------------------------

    def get_data_by_acc_num(self, acc_num):
        for entry in self.data:
            if entry['Acc_Num'] == acc_num:
                return entry

    def get_name_by_acc_num(self, acc_num):
        for entry in self.data:
            if entry['Acc_Num'] == acc_num:
                return entry['Name']

    def get_balance_by_acc_num(self, acc_num):
        for entry in self.data:
            if entry['Acc_Num'] == acc_num:
                return entry['Balance']

    def get_status_by_acc_num(self, acc_num):
        for entry in self.data:
            if entry['Acc_Num'] == acc_num:
                return entry['Status']

    # Validate ------------------------------------------------

    def validate_acc_num(self, acc_num):
        """
        Checks if the Account Number exists.
        """
        for entry in self.data:
            if entry['Acc_Num'] == acc_num:
                return True
        return False

    def validate_name(self, name):
        """
        Checks if the Name / Username exists.
        """
        for entry in self.data:
            if entry['Name'] == name:
                return True
        return False

    def validate_balance(self, acc_num, amount, is_receiving=False):
        """
        Validates whether there is enough in a specific Account balance to handle the action for the given amount.
        """
        balance = self.get_balance_by_acc_num(acc_num)
        if (not is_receiving) and (amount > balance):
            return False
        if is_receiving and (amount + balance) > 99999:
            return False
        return True

    def validate_user_and_account_num_match(self, name, account_num):
        for entry in self.data:
            if entry["Name"] == name and entry["Acc_Num"] == account_num:
                return True
        return False

    # UPDATERS ------------------------------

    def update_balance(self, acc_num, new_balance):
        """
        Updates the balance of a specific account.
        """
        for entry in self.data:
            if entry['Acc_Num'] == acc_num:
                entry['Balance'] = new_balance
                return True
        return False

    def update_name(self, acc_num, new_name):
        """
        Updates the name associated with a specific account.
        """
        for entry in self.data:
            if entry['Acc_Num'] == acc_num:
                entry['Name'] = new_name
                return True
        return False

    def update_status(self, acc_num, new_status):
        """
        Updates the status of a specific account.
        """
        for entry in self.data:
            if entry['Acc_Num'] == acc_num:
                entry['Status'] = new_status
                return True
        return False

    def save_data(self):
        """
        Saves the updated account information back to the file.
        """
        with open(self.dir, "w") as f:
            for entry in self.data:
                formatted_acc_num = entry['Acc_Num'].zfill(5)  # Ensure leading zeros
                formatted_name = entry["Name"].ljust(22, "_").replace(" ", "_")
                formatted_status = entry["Status"]
                formatted_balance = f"{entry['Balance']:10.2f}"
                f.write(f"{formatted_acc_num}{formatted_name}{formatted_status} {formatted_balance}\n")

    # Miscellaneous ---------------------------------------

    def print_all_data(self):
        for entry in self.data:
            print(f"Acc_Num:{entry['Acc_Num']} - Name:{entry['Name']} - Status:{entry['Status']} - Balance:{entry['Balance']}")

    

# def main():
#     # Initialize BankData
#     bd = BankData(dir="CurrentBankAccounts.txt")
#     bd.print_all_data()
    
#     # Print a specific Acc Num information.
#     print(bd.get_data_by_acc_num("1000"))

#     # Simulate a validation for a 10 dollar transaction.
#     print(bd.validate_balance("1000", 10))

#     print(bd.validate_user_and_account_num_match("Clark K", "1002"))


# if __name__ == "__main__": 
#    main()