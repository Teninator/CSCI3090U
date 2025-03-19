#!/bin/bash

# Root directory where test cases are stored
TEST_ROOT="../../Tests"

echo "🔍 Starting file cleanup at $(date)"

# Prompt user to choose between cleaning up all transactions or a specific one
echo "Select an option:"
echo "1. Cleanup all transactions"
echo "2. Cleanup a specific transaction"
read -p "Enter your choice (1 or 2): " choice

# Function to cleanup files for a specific transaction
cleanup_transaction() {
    TRANSACTION_NAME="$1"
    TRANSACTION_DIR="$TEST_ROOT/$TRANSACTION_NAME/"
    echo "Cleaning up transaction type: $TRANSACTION_NAME"

    # Loop through each test directory for the current transaction
    for TEST_DIR in "$TRANSACTION_DIR"*/; do
        TEST_NAME=$(basename "$TEST_DIR")  # Ensure TEST_NAME is correctly captured
        echo "Cleaning up test case: $TRANSACTION_NAME - $TEST_NAME"

        # Define the output and transaction files
        OUTPUT_FILE="$TEST_DIR/${TEST_NAME}.out.txt"
        TRANSACTION_FILE="$TEST_DIR/${TEST_NAME}.atf.txt"

        # Check if the output file exists and remove it
        if [[ -f "$OUTPUT_FILE" ]]; then
            echo "Deleting generated output file: $OUTPUT_FILE"
            rm "$OUTPUT_FILE"
        else
            echo "No output file found for test: $TEST_NAME"
        fi

        # Check if the transaction file exists and remove it
        if [[ -f "$TRANSACTION_FILE" ]]; then
            echo "Deleting generated transaction file: $TRANSACTION_FILE"
            rm "$TRANSACTION_FILE"
        else
            echo "No transaction file found for test: $TEST_NAME"
        fi
    done
}

# Handle user choice
if [[ "$choice" -eq 1 ]]; then
    # Cleanup for all transactions
    for TRANSACTION_DIR in "$TEST_ROOT"/*/; do
        TRANSACTION_NAME=$(basename "$TRANSACTION_DIR")
        cleanup_transaction "$TRANSACTION_NAME"
    done
elif [[ "$choice" -eq 2 ]]; then
    # Cleanup for a specific transaction
    echo "Available transactions:"
    # List all available transaction names
    for TRANSACTION_DIR in "$TEST_ROOT"/*/; do
        TRANSACTION_NAME=$(basename "$TRANSACTION_DIR")
        echo "- $TRANSACTION_NAME"
    done

    # Get the transaction name to clean up
    read -p "Enter the transaction name to clean up: " transaction_name
    if [[ -d "$TEST_ROOT/$transaction_name" ]]; then
        cleanup_transaction "$transaction_name"
    else
        echo "❌ Transaction '$transaction_name' not found!"
    fi
else
    echo "❌ Invalid choice! Please select 1 or 2."
fi

echo "🎯 Cleanup completed at $(date)!"
