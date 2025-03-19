---

# **Test Automation Scripts**

## **Overview**
This repository contains automation scripts to validate, clean up, and run tests for different transaction types stored in the `Tests` directory.

## **1. `validate_test_file.sh`**

### **Purpose**:  
Validates the required files for each test case and ensures that they are ready for execution.

### **Usage**:
```bash
cd Frontend/Testing_Scripts
./validate_test_file.sh
```

### **Functionality**:
- Loops through all transactions and test cases.
- Checks for the presence of the necessary files:
  - `CurrentBankAccounts.txt`
  - `Transaction files (.atf.txt and .etf.txt)`
  - `Input file (.inp.txt)`
  - `Output file (.out.txt and .bto.txt)`
- Reports the missing files for each test case and any difference in the outputs and expected outputs.

---

## **2. `delete_generated_test_files.sh`**

### **Purpose**:

Deletes the generated output and transaction files from the test cases after execution.

### **Usage**:

```bash
cd Frontend/Testing_Scripts
./delete_generated_test_files.sh
```

### **Functionality**:

- Prompts the user to choose:
  1. Cleanup for all transactions
  2. Cleanup for a specific transaction
- Loops through the test directories and deletes the following files for each test case:
  - `*.out.txt` (output files)
  - `*.atf.txt` (transaction files)

---

## **3. `test_bank_atm.sh`**

### **Purpose**:

Executes the tests for all or a specific transaction and captures the output.

### **Usage**:

```bash
cd Frontend/Testing_Scripts
./test_bank_atm.sh
```

### **Functionality**:

- Prompts the user to choose:
  1. Run tests for all transactions
  2. Run tests for a specific transaction
- For each test case:
  - Checks for the presence of required files (`CurrentBankAccounts.txt`, `*.inp.txt`).
  - Runs the test with the Python script `bank-atm.py` and captures the output in the corresponding `*.out.txt` file.

---

## **Notes**:

- Make sure to have the correct permissions to execute these scripts (use `chmod +x <script_name>` to make them executable).

---
