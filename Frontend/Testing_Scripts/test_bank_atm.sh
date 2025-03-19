#!/bin/bash

# Root directory where test cases are stored
TEST_ROOT="../../Tests"

echo "🔍 Starting test execution at $(date)"

# Default fast mode to false
FAST_MODE="false"

# Parse arguments
for arg in "$@"; do
    if [[ "$arg" == "--fast=true" ]]; then
        FAST_MODE="true"
    fi
done

# Prompt user to choose between testing all transactions or a specific one
echo "Select an option:"
echo "1. Test all transactions"
echo "2. Test a specific transaction"
read -p "Enter your choice (1 or 2): " choice

# Function to execute tests for a specific transaction
test_transaction() {
    TRANSACTION_NAME="$1"
    TRANSACTION_DIR="$TEST_ROOT/$TRANSACTION_NAME"
    echo "Entering transaction type: $TRANSACTION_NAME"

    # Loop through each test directory for the current transaction
    for TEST_DIR in "$TRANSACTION_DIR"/*/; do
        TEST_NAME=$(basename "$TEST_DIR")
        echo "Running test case: $TRANSACTION_NAME - $TEST_NAME"

        # Define file paths based on test structure
        ACCOUNTS_FILE="${TEST_DIR}CurrentBankAccounts.txt"
        TRANSACTION_FILE="${TEST_DIR}${TEST_NAME}.atf.txt"
        INPUT_FILE="${TEST_DIR}${TEST_NAME}.inp.txt"
        OUTPUT_FILE="${TEST_DIR}${TEST_NAME}.out.txt"  # Output file for capturing script output

        echo "Checking required files..."
        echo "  Accounts file: $ACCOUNTS_FILE"
        echo "  Transaction file: $TRANSACTION_FILE"
        echo "  Input file: $INPUT_FILE"
        echo "  Output file: $OUTPUT_FILE"

        # Check if all necessary files exist
        if [[ -f "$ACCOUNTS_FILE" && -f "$INPUT_FILE" ]]; then
            echo "✅ All required files found. Starting execution..."
            echo "Running: python3 bank-atm.py \"$ACCOUNTS_FILE\" \"$TRANSACTION_FILE\" < \"$INPUT_FILE\""
            python3 bank-atm.py "$ACCOUNTS_FILE" "$TRANSACTION_FILE" < "$INPUT_FILE" > "$OUTPUT_FILE" 2>&1

            EXIT_CODE=$?
            if [[ $EXIT_CODE -eq 0 ]]; then
                echo "✅ Test $TEST_NAME completed successfully. Output saved to $OUTPUT_FILE."
            else
                echo "❌ Error running test: $TEST_NAME (Exit code: $EXIT_CODE)"
            fi
        else
            echo "❌ Missing required files for test: $TEST_NAME"
        fi

        echo "-------------------------------------------"
        if [[ "$FAST_MODE" == "false" ]]; then
            read -p "Press [Enter] to run the next test or [Ctrl+C] to stop."
        fi
    done
}

# Handle user choice
if [[ "$choice" -eq 1 ]]; then
    # Test all transactions
    for TRANSACTION_DIR in "$TEST_ROOT"/*/; do
        TRANSACTION_NAME=$(basename "$TRANSACTION_DIR")
        test_transaction "$TRANSACTION_NAME"
    done
elif [[ "$choice" -eq 2 ]]; then
    # Test a specific transaction
    echo "Available transactions:"
    for TRANSACTION_DIR in "$TEST_ROOT"/*/; do
        TRANSACTION_NAME=$(basename "$TRANSACTION_DIR")
        echo "- $TRANSACTION_NAME"
    done

    read -p "Enter the transaction name to test: " transaction_name
    if [[ -d "$TEST_ROOT/$transaction_name" ]]; then
        test_transaction "$transaction_name"
    else
        echo "❌ Transaction '$transaction_name' not found!"
    fi
else
    echo "❌ Invalid choice! Please select 1 or 2."
fi

echo "🎯 All tests completed at $(date)!"
